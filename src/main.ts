import express from 'express';
import { PrismaClient } from '@prisma/client';

const port = 3000;
const app = express();
const db = new PrismaClient();

app.listen(port, () => {
	return console.log(`Express is listening at http://localhost:${port}`);
});
