type Title = {
  _id: string
  titleId: string
  titleType: string
  name: string
  nameEng: string
  genres: string[]
  isAdult: number
  startYear: number
  endYear: number
  episode?: number
  season?: number
  runtime: number
  rating: number
  votes: number
  writers: string[]
  directors: string[]
  principals: string[]
}

export default Title
