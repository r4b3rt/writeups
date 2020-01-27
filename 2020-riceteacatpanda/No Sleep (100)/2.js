var list = ["gamerfuel=Jan 27, 2020 04:20:00", "Jan 27, 2020 04:20:00", "getTime", "exec", "floor", "getElementById", "gamer timer", "AES", "decrypt", "U2FsdGVkX18kRm6FDkRVQfVuNPTxyOnJzpu8QnI/9UKoCXp6hQcley11nBnLIItj", "ok boomer", "innerHTML", "Utf8", "cookie"];
(function(a, b) {
  var c = function(d) {
    while (--d) {
      a["push"](a["shift"]());
    }
  };
  c(++b);
})(list, 0x99);
var list = ["cookie", "gamerfuel=Jan 27, 2020 04:20:00", "Jan 27, 2020 04:20:00", "getTime", "exec", "floor", "getElementById", "gamer timer", "AES", "decrypt", "U2FsdGVkX18kRm6FDkRVQfVuNPTxyOnJzpu8QnI/9UKoCXp6hQcley11nBnLIItj", "ok boomer", "innerHTML", "Utf8"];
var func = function(a, b) {
  a = a - 0x0;
  var c = list[a];
  return c;
};
//document[func("0x0")] = func("0x1");
document["cookie"] = "gamerfuel=Jan 27, 2020 04:20:00";
//var countDownDate = new Date(func("0x2"))[func("0x3")]();
var countDownDate = new Date("Jan 27, 2020 04:20:00")["getTime"]();
var x = setInterval(function() {
  //var target = new Date(/[^=]*$/[func("0x4")](document[func("0x0")])[0x0])[func("0x3")]();
  var target = new Date(/[^=]*$/["exec"](document["cookie"])[0x0])["getTime"]();
  var now = new Date()["getTime"]();
  var diff = target - now;
  //var days = Math[func("0x5")](diff / (0x3e8 * 0x3c * 0x3c * 0x18));
  var days = Math["floor"](diff / (0x3e8 * 0x3c * 0x3c * 0x18));
  //var hours = Math[func("0x5")]((diff % (0x3e8 * 0x3c * 0x3c * 0x18)) / (0x3e8 * 0x3c * 0x3c));
  var hours = Math["floor"]((diff % (0x3e8 * 0x3c * 0x3c * 0x18)) / (0x3e8 * 0x3c * 0x3c));
  //var minutes = Math[func("0x5")]((diff % (0x3e8 * 0x3c * 0x3c)) / (0x3e8 * 0x3c));
  var minutes = Math["floor"]((diff % (0x3e8 * 0x3c * 0x3c)) / (0x3e8 * 0x3c));
  var seconds = Math["floor"]((diff % (0x3e8 * 0x3c)) / 0x3e8);
  //document[func("0x6")](func("0x7"))["innerHTML"] = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
  document["getElementById"]("gamer timer")["innerHTML"] = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
  if (diff < 0x0) {
    clearInterval(x);
    //var answer = CryptoJS[_0x2ad1("0x8")][_0x2ad1("0x9")](_0x2ad1("0xa"), _0x2ad1("0xb"));
    var answer = CryptoJS["AES"]["decrypt"]("U2FsdGVkX18kRm6FDkRVQfVuNPTxyOnJzpu8QnI/9UKoCXp6hQcley11nBnLIItj", "ok boomer");
    //document[func("0x6")](func("0x7"))[func("0xc")] = answer["toString"](CryptoJS["enc"][func("0xd")]);
    document["getElementById"]("gamer timer")["innerHTML"] = answer["toString"](CryptoJS["enc"]["Utf8"]);
  }
}, 0x3e8);
