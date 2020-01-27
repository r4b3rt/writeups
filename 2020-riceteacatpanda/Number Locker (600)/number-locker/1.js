function guess() {
  try {
    alert(
      eval(
        // "String.raw`rplUD1U}0WNU}Wm}T0}Nm}u02}3U`.split``.map(i=>([a,b,c]='"
        atob(
          "U3RyaW5nLnJhd2BycIFsmVVEMVV9lTBXTlV9V219VDCAfU5tlX11MDJ9M1WfYC5zcGxpdGBgLm1hcChpPT4oW2EsYixjXT0n????Jy5zcGxpdGBgLm1hcChpPT5pLmNoYXJDb2RlQXQoKSksU3RyaW5nKS5mcm9tQ2hhckNvZGUoKChhLWkuY2hhckNvZGVBdCgpKV5iKStjKSkuam9pbmBg".replace(
            /\?\?\?\?/,
            (s["value"] | 0)
              .toString(16)
              .match(/.{2}/g)
              .map(i => String["fromCharCode"](eval("+('0x'+i)"))).join``
          )
        )
      )
    );
  } catch (e) {}
}
