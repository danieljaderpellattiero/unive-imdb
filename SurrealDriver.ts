import readline from 'readline';
import { createReadStream, readFileSync, access, constants } from 'fs';
import { Surreal, ConnectionOptions, Engine } from 'surrealdb.js';

class SurrealDriver {
	static #instance: SurrealDriver | null = null;
	#database: Surreal | null = null;
	#connection: Engine | undefined = undefined;
	#imdb: Map<string, string> = new Map([
		['name.basics.tsv', 'https://datasets.imdbws.com/name.basics.tsv.gz'],
		['title.akas.tsv', 'https://datasets.imdbws.com/title.akas.tsv.gz'],
		['title.basics.tsv', 'https://datasets.imdbws.com/title.basics.tsv.gz'],
		['title.crew.tsv', 'https://datasets.imdbws.com/title.crew.tsv.gz'],
		['title.episode.tsv', 'https://datasets.imdbws.com/title.episode.tsv.gz'],
		['title.principals.tsv', 'https://datasets.imdbws.com/title.principals.tsv.gz'],
		['title.ratings.tsv', 'https://datasets.imdbws.com/title.ratings.tsv.gz'],
	]);

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
			`DEFINE USER IF NOT EXISTS ${username} ON DATABASE PASSWORD "${password}" ROLES EDITOR;`
		);
	}

	public async signIn(username: string, password: string): Promise<void> {
		await this.#database!.signin({ username, password });
	}

	public async createTables(): Promise<void> {
		const schemas: string[] = [];
		const schemasQueries: Promise<void>[] = [];
		const schemasAvailable: Promise<boolean>[] = [];
		for (const table of this.#imdb.keys()) {
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

	public async disconnect(): Promise<void> {
		await this.#database!.close();
	}
}

export default SurrealDriver;
