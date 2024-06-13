import 'dotenv/config';
import express from 'express';
const { MongoClient } = require('mongodb');

const app = express();
const client = new MongoClient(process.env.DATABASE_URL);

app.get('/search/preview/:title', async (req, res) => {
	try {
		await client.connect();
		const pipeline = await client
			.db('unive-imdb')
			.collection('title.akas')
			.aggregate([
				{ $match: { nameLower: { $regex: new RegExp(`^${req.params.title}`) } } },
				{ $group: { _id: '$titleId' } },
				{ $lookup: { from: 'title.basics', localField: '_id', foreignField: '_id', as: 'ref_basic' } },
				{ $lookup: { from: 'title.episodes', localField: '_id', foreignField: '_id', as: 'ref_episode' } },
				{
					$project: {
						_id: 0,
						titleId: {
							$ifNull: [{ $arrayElemAt: ['$ref_episode._id', 0] }, '$_id'],
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
			])
			.toArray();
		res.status(200).send(pipeline);
	} catch (err: any) {
		res.status(500).send(err.message);
	} finally {
		await client.close();
	}
});

app.get('/search/:title', async (req, res) => {
	const page = parseInt(req.query.page as string) || 1;
	const itemsPerPage = parseInt(req.query.itemsPerPage as string) || 10;
	try {
		await client.connect();
		const pipeline = await client
			.db('unive-imdb')
			.collection('title.akas')
			.aggregate([
				{ $match: { nameLower: { $regex: new RegExp(`^${req.params.title}`) } } },
				{ $group: { _id: '$titleId' } },
				{ $lookup: { from: 'title.basics', localField: '_id', foreignField: '_id', as: 'ref_basic' } },
				{ $lookup: { from: 'title.episodes', localField: '_id', foreignField: '_id', as: 'ref_episode' } },
				{
					$project: {
						_id: 0,
						titleId: {
							$ifNull: [{ $arrayElemAt: ['$ref_episode._id', 0] }, '$_id'],
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
			])
			.toArray();
		res.status(200).send(pipeline);
	} catch (err: any) {
		res.status(500).send(err.message);
	} finally {
		await client.close();
	}
});

app.get('/title/:id', async (req, res) => {
	try {
		await client.connect();
		const pipeline = await client
			.db('unive-imdb')
			.collection('title.basics')
			.aggregate([
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
										$and: [
											{ $eq: ['$titleId', '$$titleId'] },
											{ $ne: ['$job', 'director'] },
											{ $ne: ['$job', 'writer'] },
										],
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
			])
			.toArray();
		res.status(200).send(pipeline);
	} catch (err: any) {
		res.status(500).send(err.message);
	} finally {
		await client.close();
	}
});

app.get('/episode/:id', async (req, res) => {
	try {
		await client.connect();
		const pipeline = await client
			.db('unive-imdb')
			.collection('title.episodes')
			.aggregate([
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
										$and: [
											{ $eq: ['$titleId', '$$titleId'] },
											{ $ne: ['$job', 'director'] },
											{ $ne: ['$job', 'writer'] },
										],
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
			])
			.toArray();
		res.status(200).send(pipeline);
	} catch (err: any) {
		res.status(500).send(err.message);
	} finally {
		await client.close();
	}
});

app.listen(process.env.PORT, () => {
	return console.log(`Express is listening at http://localhost:${process.env.PORT}`);
});
