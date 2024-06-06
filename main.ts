import chalk from 'chalk';
import SurrealDriver from './SurrealDriver.js';

const log = console.log;
chalk.level = 3;

async function main() {
	const db = SurrealDriver.getInstance();
	try {
		await db.connect('http://localhost:8000');
		await db.setContext('unive', 'imdb');
		log(chalk.green('SurrealDB connected.'));
	} catch (error: any) {
		log(chalk.red('SurrealDB unreachable.'));
		process.exit(1);
	}
	try {
		await db.signIn('whoami', 'root');
		log(chalk.green('Root user signed in.'));
	} catch (error: any) {
		log(chalk.red('Root user signin failed.'));
		process.exit(1);
	}
	try {
		log(chalk.yellow.italic('Creating users for namespace <unive> and database <imdb>'));
		await db.createUser('mlotto', 'j7YoSESu1r6Cha0hUpR');
		log(chalk.green('\t > mlotto | j7YoSESu1r6Cha0hUpR$'));
		await db.createUser('djader', 'B0g-spi!8EBr?9ADReTl');
		log(chalk.green('\t > djader | B0g-spi!8EBr?9ADReTl'));
		log(chalk.green('Users created successfully.'));
	} catch (error: any) {
		if (error.message.includes('already exists')) {
			log(chalk.green('Users already created.'));
		} else {
			log(chalk.red('User creation failed.'));
			process.exit(1);
		}
	}
	try {
		await db.createTables();
		log(chalk.green('Tables created successfully.'));
	} catch (error: any) {
		if (error.message.includes('already exists')) {
			log(chalk.green('Tables already created.'));
		} else {
			log(chalk.red('Tables creation failed.'));
			process.exit(1);
		}
	}
	try {
		await db.insertTitles();
		log(chalk.green('Titles inserted successfully.'));
	} catch (error: any) {
		log(chalk.red('Titles insertion failed.'));
	}
	try {
		await db.insertRatings();
		log(chalk.green('Ratings inserted successfully.'));
	} catch (error: any) {
		log(chalk.red('Ratings insertion failed.'));
	}
	process.exit(0);
}

main();
