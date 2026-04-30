const express = require('express');
const app = express();

app.get('/', (req, res) => {
 res.send('Hello! Updated automatically you doing a fantastic job god bless you hahah! 🔥');
});

app.listen(3000, () => console.log('Running on port 3000'));