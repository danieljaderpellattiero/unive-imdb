import readline from 'readline';
import { Surreal, ConnectionOptions, Engine } from 'surrealdb.js';
import { createReadStream, readFileSync, access, constants } from 'fs';

class SurrealDriver {
	static #instance: SurrealDriver | null = null;
	#database: Surreal | null = null;
	#connection: Engine | undefined = undefined;
	#imdbDatasets: string[] = ['title.basics.tsv', 'title.ratings.tsv'];

	private constructor() {
		this.#database = new Surreal();
	}

	public static getInstance(): SurrealDriver {
		if (!SurrealDriver.#instance) {
			SurrealDriver.#instance = new SurrealDriver();
		}
		return SurrealDriver.#instance;
	}

	public async connect(url: string, options?: ConnectionOptions): Promise<void> {
		await this.#database!.connect(url, options);
		this.#connection = this.#database!.connection;
	}

	private checkConnection(): void {
		console.log(this.#connection ? this.#connection.connection : 'No connection established.');
	}

	public async setContext(namespace: string, database: string): Promise<void> {
		await this.#database!.use({ namespace, database });
	}

	public async createUser(username: string, password: string): Promise<void> {
		await this.#database!.query(
			`DEFINE USER IF NOT EXISTS ${username} ON NAMESPACE PASSWORD "${password}" ROLES EDITOR;`
		);
	}

	public async signIn(username: string, password: string): Promise<void> {
		await this.#database!.signin({ username, password });
	}

	public async createTables(): Promise<void> {
		const schemas: string[] = [];
		const schemasQueries: Promise<void>[] = [];
		const schemasAvailable: Promise<boolean>[] = [];
		for (const table of this.#imdbDatasets) {
			if (table !== 'title.crew.tsv') {
				const tableAlias = `${table.slice(0, table.lastIndexOf('.')).replace('.', '_')}.sql`;
				schemas.push(tableAlias);
				schemasAvailable.push(
					new Promise((resolve) => {
						access(`./schemas/${tableAlias}`, constants.R_OK, (err) => resolve(!err));
					})
				);
			}
		}
		if ((await Promise.all(schemasAvailable)).every((v) => v)) {
			for (const schema of schemas) {
				schemasQueries.push(
					new Promise(async (resolve, reject) => {
						try {
							await this.#database!.query(readFileSync(`./schemas/${schema}`, 'utf-8'));
							resolve();
						} catch (error: any) {
							reject(error);
						}
					})
				);
			}
			await Promise.all(schemasQueries);
		} else {
			throw new Error();
		}
	}

	public async insertTitles(): Promise<void> {
		const stream = createReadStream('./data/title.basics.tsv');
		const reader = readline.createInterface({ input: stream, crlfDelay: Infinity });
		let header: boolean = true;
		for await (const line of reader) {
			if (!header) {
				const entry = this.sanitizeTitles(line);
				await this.#database!.create('title_basics', {
					id: entry[0],
					titleType: entry[1],
					primaryTitle: entry[2],
					originalTitle: entry[3],
					isAdult: entry[4],
					startYear: entry[5],
					endYear: entry[6],
					runtimeMinutes: entry[7],
					genres: entry[8],
					akas: [],
					episodes: [],
					ratings: [],
					directors: [],
					writers: [],
					principals: [],
				});
			} else {
				header = false;
			}
		}
	}

	private sanitizeTitles(line: string): any[] {
		return line
			.split('\t')
			.map((field: string, index: number) =>
				field === '\\N'
					? index === 8
						? []
						: undefined
					: !isNaN(Number(field))
					? index === 2 || index === 3
						? field
						: index === 4
						? Boolean(parseInt(field))
						: field.indexOf('.') !== -1
						? parseFloat(field)
						: parseInt(field)
					: index === 8 && typeof field === 'string'
					? [field]
					: field
			);
	}

	public async insertRatings(): Promise<void> {
		const stream = createReadStream('./data/title.ratings.tsv');
		const reader = readline.createInterface({ input: stream, crlfDelay: Infinity });
		let header: boolean = true;
		for await (const line of reader) {
			if (!header) {
				const entry = this.sanitizeRatings(line);
				const { tb, id } = (
					await this.#database!.create('title_ratings', {
						averageRating: entry[1],
						numVotes: entry[2],
					})
				)[0].id;
				await this.#database!.query(`UPDATE title_basics:${entry[0]} SET ratings += ${tb}:${id}`);
			} else {
				header = false;
			}
		}
	}

	private sanitizeRatings(line: string): any[] {
		return line
			.split('\t')
			.map((field: string) =>
				!isNaN(Number(field)) ? (field.indexOf('.') !== -1 ? parseFloat(field) : parseInt(field)) : field
			);
	}

	public async disconnect(): Promise<void> {
		await this.#database!.close();
	}
}

export default SurrealDriver;
