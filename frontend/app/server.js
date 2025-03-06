const express = require('express');
const path = require('path');

const app = express();
const port = 3000;

// Statisches Verzeichnis für HTML-Dateien, CSS, etc.
app.use(express.static(path.join(__dirname, 'public')));

app.listen(port, () => {
  console.log(`Server läuft auf Port ${port}`);
});
