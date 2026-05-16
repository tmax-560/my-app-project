const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// 1. Tell Express to serve everything in the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// 2. Route to serve the index.html specifically
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`Portfolio running at http://localhost:${port}`);
});