// String.raw`rp\x81l\x99UD1U}\x950WNU}Wm}T0\x80}Nm\x95}u02}3U\x9f`.split``
let blah = Buffer.from("cnCBbJlVRDFVfZUwV05VfVdtfVQwgH1ObZV9dTAyfTNVnw==", "base64").toString().split``;

// .map(i=>([a,b,c]='
for (var i = 0; i < 256; i++) {
  for (var j = 0; j < 256; j++) {
    for (var k = 0; k < 256; k++) {
      let s = blah.map(zz => (([a, b, c] = [i, j, k]), String).fromCharCode(((a - zz.charCodeAt()) ^ b) + c)).join``;
      if (s.includes("rtcp")) {
        console.log(s);
        console.log(i, j, k);
        process.exit(0);
      }
    }
  }
}
