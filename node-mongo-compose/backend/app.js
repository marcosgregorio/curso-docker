const express = require('express')
const restful = require('node-restful')
const bodyParser = require('body-parser')
const cors = require('cors')
const server = express()
const mongoose = restful.mongoose

mongoose.Promise = global.Promise
mongoose.connect('mongodb://db/mydb')

server.get('/', (req, res, next) => res.send('Backend'))


// midlewares

server.use(bodyParser.urlencoded({entended: true}))
server.use(bodyParser.json())
server.use(cors())

// ODM
const Client = restful.model('CLient', {
	name: { type: String, required: true }
})

Client.methods(['get', 'post', 'put', 'delete'])
Client.updateOptions({new: true, runValidators: true})

Client.register(server, '/clients')

server.listen(3000)
