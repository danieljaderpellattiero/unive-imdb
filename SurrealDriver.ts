import { Surreal, ConnectionOptions, Engine } from 'surrealdb.js';

class SurrealDriver {
	static #instance: SurrealDriver | null = null;
	static #imdbDataFiles: string[] = [
		'name.basics.tsv',
		'title.akas.tsv',
		'title.basics.tsv',
		'title.crew.tsv',
		'title.episode.tsv',
		'title.principals.tsv',
		'title.ratings.tsv',
	];
	#database: Surreal | null = null;
	#connection: Engine | undefined = undefined;

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

	public async disconnect(): Promise<void> {
		await this.#database!.close();
	}
}

export default SurrealDriver;
