// ==UserScript==
// @name      FairyJoke Jackets on Kamai
// @version   1
// @updateURL https://github.com/Tina-otoge/FairyJokeAPI/raw/userscripts-test/userscripts/kamai.user.js
// @include   https://kamaitachi.xyz/*
// ==/UserScript==


setInterval(main, 2000);
const matcher_link = "https://kamaitachi.xyz/dashboard/games/sdvx/Single/songs/";
const diff_map = {
  "NOV": "NOVICE",
  "ADV": "ADVANCED",
  "EXH": "EXHAUST",
  "MXM": "MAXIMUM",
  "INF": "INFINITE",
  "GRV": "GRAVITY",
  "HVN": "HEAVENLY",
  "VVD": "VIVID",
};

function main () {
  document.querySelectorAll('tr').forEach(tr => {
    tr.querySelectorAll('td').forEach(td => {
      if (!tr.dataset.jacketed) {
        td.querySelectorAll('a').forEach(a => {
          if (a.href.startsWith(matcher_link)) {
            let parts = a.href.split('/');
            let id = parts[8];
            let diff = diff_map[parts[9]];
            let url = `https://fairyjoke.tina.moe/api/games/sdvx/musics/${id}/${diff}.png`;
            let first_cell = tr.children.item(0);
            let img = document.createElement('img');
            img.src = url;
            img.width = 100;
            img.height = 100;
            img.style.float = 'left';
            a.style.display = 'block';
            td.appendChild(img);
            tr.dataset.jacketed = true;
          }
        });
      }
    });
  });
}
