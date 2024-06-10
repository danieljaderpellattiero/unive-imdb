# SurrealDB

## Installation

> All the scripts have to be run inside the **Powershell** or **Windows Terminal** (_for Windows users_); standard **CLI** otherwise.

### Windows

Download the latest version of the database.

```sh
iwr https://windows.surrealdb.com -useb | iex
```

It installs the database inside `C:\Program Files\SurrealDB`, falling back to a user-specified folder if necessary.

Update to the latest version.

```sh
iwr https://windows.surrealdb.com -useb | iex
```

### Linux

Download the latest version of the database.

```sh
curl -sSf https://install.surrealdb.com | sh
```

It installs the database inside `/usr/local/bin`, falling back to a user-specified folder if necessary.

Update to the latest version.

```sh
curl -sSf https://install.surrealdb.com | sh
```

---

Finally check whether the installation was successful.

```sh
surreal help
```

The SurrealDB command-line tool was installed successfully if the output on your terminal looks like this:

```sh
.d8888b.                                             888 8888888b.  888888b.
d88P  Y88b                                            888 888  'Y88b 888  '88b
Y88b.                                                 888 888    888 888  .88P
 'Y888b.   888  888 888d888 888d888  .d88b.   8888b.  888 888    888 8888888K.
	'Y88b. 888  888 888P'   888P'   d8P  Y8b     '88b 888 888    888 888  'Y88b
	  '888 888  888 888     888     88888888 .d888888 888 888    888 888    888
Y88b  d88P Y88b 888 888     888     Y8b.     888  888 888 888  .d88P 888   d88P
 'Y8888P'   'Y88888 888     888      'Y8888  'Y888888 888 8888888P'  8888888P'


SurrealDB command-line interface and server

To get started using SurrealDB, and for guides on connecting to and building applications
on top of SurrealDB, check out the SurrealDB documentation (https://surrealdb.com/docs).

If you have questions or ideas, join the SurrealDB community (https://surrealdb.com/community).

If you find a bug, submit an issue on Github (https://github.com/surrealdb/surrealdb/issues).

We would love it if you could star the repository (https://github.com/surrealdb/surrealdb).

----------

USAGE:
	surreal [SUBCOMMAND]

OPTIONS:
	-h, --help    Print help information

SUBCOMMANDS:
	start      Start the database server
	import     Import a SQL script into an existing database
	export     Export an existing database into a SQL script
	version    Output the command-line tool version information
	sql        Start an SQL REPL in your terminal with pipe support
	help       Print this message or the help of the given subcommand(s)

```

## Run the database

### On-disk single node (local instance)

Boot the SurrealDB service.

```sh
surreal start --log trace --auth --user whoami --pass root --bind 127.0.0.1:8000 file:unive-imdb.db
```

#### Data insertion - method №1

1. Download IMDb data from the [website](https://datasets.imdbws.com/).
2. Extract the _.tsv_ files and produce the reduced version using the **DatasetChunker**.
3. Move the reduced version of the _.tsv_ files into the _data_ folder.

Install [Node.js](https://nodejs.org/en) and then TypeScript. (globally)

```sh
npm install -g typescript
```

Install the project dependences.

```sh
npm install
```

Run Typescript.

```sh
tsc || tsc -w
```

Run the script.

```sh
node main.js
```

_Once the script ends the database is ready and accessible from [Surrealist](https://surrealdb.com/surrealist)._

#### Data insertion - method №2

1. Open Surrealist.
2. Navigate into the **Explorer** section on the left sidebar.
3. Click on _Import data_ and select the **imdb.surql** file.

### Docker

... _coming soon._
