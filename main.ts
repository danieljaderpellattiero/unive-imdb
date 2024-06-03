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
		await db.createUser('mlotto', '&15o1=o+0ATU!7slW$oM');
		log(chalk.green('\t > mlotto | &15o1=o+0ATU!7slW$oM'));
		await db.createUser('djader', '=r#rip8mo!l$hov!cE2r');
		log(chalk.green('\t > djader | =r#rip8mo!l$hov!cE2r'));
		log(chalk.green('Users created successfully.'));
	} catch (error: any) {
		if (error.message.includes('already exists')) {
			log(chalk.green('Users already created.'));
		} else {
			log(chalk.red('User creation failed.'));
			process.exit(1);
		}
	}
	process.exit(0);
}

main();
