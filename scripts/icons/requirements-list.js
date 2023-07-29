const fs = require('fs')
const path = require('path')

const run = () => {    
    const requirements = fs.readFileSync(path.resolve(__dirname, '../requirements.txt'), 'utf8').split('\n')
    console.log(requirements.join(","))
}

run();
