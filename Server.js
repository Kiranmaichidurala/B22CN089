const express = require("express");
const bodyParser = require("body-parser");
const crypto = require("crypto");

const app = express();
app.use(bodyParser.json());

// In-memory database
let urls = {};
app.post("/shorturls", (req, res) => {
  const { url, shortcode } = req.body;

  if (!url) {
    return res.status(400).json({ error: "URL is required" });
  }

  // If no shortcode provided, generate one
  const code = shortcode || crypto.randomBytes(3).toString("hex");

  urls[code] = url;

  res.json({
    message: "Short URL created successfully",
    shortUrl: `http://localhost:3000/${code}`
  });
});
app.get("/:code", (req, res) => {
  const code = req.params.code;
  const longUrl = urls[code];

  if (!longUrl) {
    return res.status(404).json({ error: "Shortcode not found" });
  }

  res.redirect(longUrl);
});

app.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
