import 'dotenv/config';
import pino from 'pino';
import express from 'express';
import pinoHttp from 'pino-http';
const cors = require('cors');
const { MongoClient } = require('mongodb');

const client = new MongoClient(process.env.DATABASE_URL);
const fileTransport = pino.transport({
	target: 'pino/file',
	options: {
		mkdir: true,
		destination: `logs/${process.argv[2]}.log`,
	},
});
const logger = pinoHttp(
	{
		base: null,
		autoLogging: false,
		level: process.env.LOG_LEVEL || 'info',
		serializers: {
			req(req) {
				return {
					id: req.id,
					method: req.method,
					url: req.url,
				};
			},
			res() {
				return {};
			},
		},
		timestamp: pino.stdTimeFunctions.isoTime,
	},
	fileTransport
);
let connection: any;
let db: any;

const app = express();

app.use(cors());
app.use(logger);

// Starts the server and connect to the database.
app.listen(process.env.PORT, async () => {
	try {
		if(process.argv[2]) {
			connection = await client.connect();
			db = connection.db('unive-imdb');
			await db.command({ profile: 2 });
		} else {
			console.log('Please provide a name for the log file.')
			process.exit(1);
		}
	} catch (err: any) {
		process.exit(1);
	}
});

// Returns the top 4 most voted titles that match the search query prefix.
app.get('/search/preview/:title', async (req, res) => {
	const apiServiceTime1S = Date.now();
	const pipeline = [
		{ $match: { nameLower: { $regex: new RegExp(`^${req.params.title}`) } } },
		{ $group: { _id: '$titleId' } },
		{ $lookup: { from: 'title.basics', localField: '_id', foreignField: '_id', as: 'ref_basic' } },
		{ $lookup: { from: 'title.episodes', localField: '_id', foreignField: '_id', as: 'ref_episode' } },
		{
			$project: {
				_id: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode._id', 0] }, { $arrayElemAt: ['$ref_basic._id', 0] }],
				},
				titleId: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.titleId', 0] }, null],
				},
				nameEng: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.nameEng', 0] }, { $arrayElemAt: ['$ref_episode.nameEng', 0] }],
				},
				titleType: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.titleType', 0] }, 'episode'],
				},
				startYear: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.startYear', 0] }, { $arrayElemAt: ['$ref_episode.startYear', 0] }],
				},
				endYear: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.endYear', 0] }, { $arrayElemAt: ['$ref_episode.endYear', 0] }],
				},
				season: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.season', 0] }, null],
				},
				episode: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.episode', 0] }, null],
				},
				votes: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.votes', 0] }, { $arrayElemAt: ['$ref_episode.votes', 0] }],
				},
				rating: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.rating', 0] }, { $arrayElemAt: ['$ref_episode.rating', 0] }],
				},
			},
		},
		{ $sort: { votes: -1 } },
		{ $limit: 4 },
	];
	try {
		const collection = db.collection('title.akas');
		const cursor = collection.aggregate(pipeline);
		const apiServiceTime1E = Date.now() - apiServiceTime1S;
		const apiServiceTime2S = Date.now();
		const result = await cursor.toArray();
		res.status(200).send(result);
		const apiServiceTime2E = Date.now() - apiServiceTime2S;
		const dbServiceTime = (await db.collection('system.profile').find({}).sort({ ts: -1 }).limit(1).toArray())[0]
			.millis;
		req.log.info({
			apiServiceTime: apiServiceTime1E,
			dbServiceTime,
			apiExtraServiceTime: apiServiceTime2E - dbServiceTime,
		});
	} catch (error: any) {
		req.log.error({ error: error.message });
		res.status(500).send({ error: error.message });
	}
});

// Returns the titles that match the search query prefix, paginated.
app.get('/search/:title', async (req, res) => {
	const apiServiceTime1S = Date.now();
	const page = parseInt(req.query.page as string) || 1;
	const itemsPerPage = parseInt(req.query.itemsPerPage as string) || 8;
	const pipeline = [
		{ $match: { nameLower: { $regex: new RegExp(`^${req.params.title}`) } } },
		{ $group: { _id: '$titleId' } },
		{ $lookup: { from: 'title.basics', localField: '_id', foreignField: '_id', as: 'ref_basic' } },
		{ $lookup: { from: 'title.episodes', localField: '_id', foreignField: '_id', as: 'ref_episode' } },
		{
			$project: {
				_id: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode._id', 0] }, { $arrayElemAt: ['$ref_basic._id', 0] }],
				},
				titleId: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.titleId', 0] }, null],
				},
				nameEng: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.nameEng', 0] }, { $arrayElemAt: ['$ref_episode.nameEng', 0] }],
				},
				titleType: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.titleType', 0] }, 'episode'],
				},
				startYear: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.startYear', 0] }, { $arrayElemAt: ['$ref_episode.startYear', 0] }],
				},
				endYear: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.endYear', 0] }, { $arrayElemAt: ['$ref_episode.endYear', 0] }],
				},
				season: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.season', 0] }, null],
				},
				episode: {
					$ifNull: [{ $arrayElemAt: ['$ref_episode.episode', 0] }, null],
				},
				votes: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.votes', 0] }, { $arrayElemAt: ['$ref_episode.votes', 0] }],
				},
				rating: {
					$ifNull: [{ $arrayElemAt: ['$ref_basic.rating', 0] }, { $arrayElemAt: ['$ref_episode.rating', 0] }],
				},
			},
		},
		{ $sort: { votes: -1 } },
		{ $skip: (page - 1) * itemsPerPage },
		{ $limit: itemsPerPage },
	];
	try {
		const collection = db.collection('title.akas');
		const cursor = collection.aggregate(pipeline);
		const apiServiceTime1E = Date.now() - apiServiceTime1S;
		const apiServiceTime2S = Date.now();
		const result = await cursor.toArray();
		res.status(200).send(result);
		const apiServiceTime2E = Date.now() - apiServiceTime2S;
		const dbServiceTime = (await db.collection('system.profile').find({}).sort({ ts: -1 }).limit(1).toArray())[0]
			.millis;
		req.log.info({
			apiServiceTime: apiServiceTime1E,
			dbServiceTime,
			apiExtraServiceTime: apiServiceTime2E - dbServiceTime,
		});
	} catch (error: any) {
		req.log.error({ error: error.message });
		res.status(500).send({ error: error.message });
	}
});

// Returns the list of episodes of a title, paginated.
app.get('/search/episodes/:title', async (req, res) => {
	const apiServiceTime1S = Date.now();
	const page = parseInt(req.query.page as string) || 1;
	const itemsPerPage = parseInt(req.query.itemsPerPage as string) || 8;
	const pipeline = [
		{ $match: { titleId: req.params.title } },
		{
			$project: {
				_id: 1,
				titleId: 1,
				nameEng: 1,
				startYear: 1,
				endYear: 1,
				season: 1,
				episode: 1,
				votes: 1,
				rating: 1,
			},
		},
		{ $sort: { season: -1, episode: -1 } },
		{ $skip: (page - 1) * itemsPerPage },
		{ $limit: itemsPerPage },
	];
	try {
		const collection = db.collection('title.episodes');
		const cursor = collection.aggregate(pipeline);
		const apiServiceTime1E = Date.now() - apiServiceTime1S;
		const apiServiceTime2S = Date.now();
		const result = await cursor.toArray();
		res.status(200).send(result);
		const apiServiceTime2E = Date.now() - apiServiceTime2S;
		const dbServiceTime = (await db.collection('system.profile').find({}).sort({ ts: -1 }).limit(1).toArray())[0]
			.millis;
		req.log.info({
			apiServiceTime: apiServiceTime1E,
			dbServiceTime,
			apiExtraServiceTime: apiServiceTime2E - dbServiceTime,
		});
	} catch (error: any) {
		req.log.error({ error: error.message });
		res.status(500).send({ error: error.message });
	}
});

// Returns the title details.
app.get('/title/:id', async (req, res) => {
	const apiServiceTime1S = Date.now();
	const pipeline = [
		{ $match: { _id: req.params.id } },
		{ $lookup: { from: 'title.episodes', localField: '_id', foreignField: '_id', as: 'ref_episode' } },
		{ $lookup: { from: 'title.crew', localField: '_id', foreignField: '_id', as: 'ref_crew' } },
		{
			$lookup: { from: 'name.basics', localField: 'ref_crew.directors', foreignField: '_id', as: 'ref_directors' },
		},
		{ $lookup: { from: 'name.basics', localField: 'ref_crew.writers', foreignField: '_id', as: 'ref_writers' } },
		{
			$lookup: {
				from: 'title.principals',
				let: { titleId: '$_id' },
				pipeline: [
					{
						$match: {
							$expr: {
								$and: [{ $eq: ['$titleId', '$$titleId'] }, { $ne: ['$job', 'director'] }, { $ne: ['$job', 'writer'] }],
							},
						},
					},
				],
				as: 'ref_principals',
			},
		},
		{
			$lookup: {
				from: 'name.basics',
				localField: 'ref_principals.personId',
				foreignField: '_id',
				as: 'ref_principals_basics',
			},
		},
		{
			$project: {
				_id: 0,
				titleId: '$_id',
				titleType: 1,
				nameEng: 1,
				name: 1,
				isAdult: 1,
				startYear: 1,
				endYear: 1,
				runtime: 1,
				genres: 1,
				rating: 1,
				votes: 1,
				directors: '$ref_directors.fullName',
				writers: '$ref_writers.fullName',
				principals: '$ref_principals_basics.fullName',
			},
		},
	];
	try {
		const collection = db.collection('title.basics');
		const cursor = collection.aggregate(pipeline);
		const apiServiceTime1E = Date.now() - apiServiceTime1S;
		const apiServiceTime2S = Date.now();
		const result = await cursor.toArray();
		res.status(200).send(result);
		const apiServiceTime2E = Date.now() - apiServiceTime2S;
		const dbServiceTime = (await db.collection('system.profile').find({}).sort({ ts: -1 }).limit(1).toArray())[0]
			.millis;
		req.log.info({
			apiServiceTime: apiServiceTime1E,
			dbServiceTime,
			apiExtraServiceTime: apiServiceTime2E - dbServiceTime,
		});
	} catch (error: any) {
		req.log.error({ error: error.message });
		res.status(500).send({ error: error.message });
	}
});

// Returns the episode details.
app.get('/episode/:id', async (req, res) => {
	const apiServiceTime1S = Date.now();
	const pipeline = [
		{ $match: { _id: req.params.id } },
		{ $lookup: { from: 'title.crew', localField: '_id', foreignField: '_id', as: 'ref_crew' } },
		{
			$lookup: { from: 'name.basics', localField: 'ref_crew.directors', foreignField: '_id', as: 'ref_directors' },
		},
		{ $lookup: { from: 'name.basics', localField: 'ref_crew.writers', foreignField: '_id', as: 'ref_writers' } },
		{
			$lookup: {
				from: 'title.principals',
				let: { titleId: '$_id' },
				pipeline: [
					{
						$match: {
							$expr: {
								$and: [{ $eq: ['$titleId', '$$titleId'] }, { $ne: ['$job', 'director'] }, { $ne: ['$job', 'writer'] }],
							},
						},
					},
				],
				as: 'ref_principals',
			},
		},
		{
			$lookup: {
				from: 'name.basics',
				localField: 'ref_principals.personId',
				foreignField: '_id',
				as: 'ref_principals_basics',
			},
		},
		{
			$project: {
				_id: 0,
				titleId: 1,
				season: 1,
				episode: 1,
				nameEng: 1,
				name: 1,
				isAdult: 1,
				startYear: 1,
				endYear: 1,
				runtime: 1,
				genres: 1,
				rating: 1,
				votes: 1,
				directors: '$ref_directors.fullName',
				writers: '$ref_writers.fullName',
				principals: '$ref_principals_basics.fullName',
			},
		},
	];
	try {
		const collection = db.collection('title.episodes');
		const cursor = collection.aggregate(pipeline);
		const apiServiceTime1E = Date.now() - apiServiceTime1S;
		const apiServiceTime2S = Date.now();
		const result = await cursor.toArray();
		res.status(200).send(result);
		const apiServiceTime2E = Date.now() - apiServiceTime2S;
		const dbServiceTime = (await db.collection('system.profile').find({}).sort({ ts: -1 }).limit(1).toArray())[0]
			.millis;
		req.log.info({
			apiServiceTime: apiServiceTime1E,
			dbServiceTime,
			apiExtraServiceTime: apiServiceTime2E - dbServiceTime,
		});
	} catch (error: any) {
		req.log.error({ error: error.message });
		res.status(500).send({ error: error.message });
	}
});

process.on('SIGINT', async () => {
	await gracefulShutdown();
});

process.on('SIGTERM', async () => {
	await gracefulShutdown();
});

process.on('SIGQUIT', async () => {
	await gracefulShutdown();
});

const gracefulShutdown = async () => {
	console.log('Shutting down...');
	await db.command({ profile: 0 });
	await db.collection('system.profile').drop();
	await client.close();
	process.exit(0);
};