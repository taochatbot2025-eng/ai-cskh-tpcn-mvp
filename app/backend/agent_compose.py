<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"/>
  <title>Hệ sinh thái TPCN thiên nhiên • Tư vấn & Đặt hàng cùng AI</title>
  <meta name="description" content="Landing page thương mại cho hệ sinh thái thực phẩm chức năng thiên nhiên. Tư vấn thông minh cùng Trợ lý AI và đặt hàng nhanh (COD/CK)."/>
  <style>
    :root{
      /* ===== Natural commerce palette 🌿 ===== */
      --bg:#f6f8f3;
      --card:#ffffff;
      --text:#111827;
      --muted:#6b7280;
      --line:rgba(17,24,39,.10);

      --primary:#2f6f4e;
      --primary2:#24563c;
      --accent:#6fbf8f;
      --soft:#eef6f0;
      --warn:#b45309;
      --danger:#b91c1c;

      --shadow: 0 18px 48px rgba(17,24,39,.12);
      --shadow2: 0 10px 24px rgba(47,111,78,.20);
      --r:18px;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      color:var(--text);
      background:
        radial-gradient(900px 500px at 10% -10%, rgba(111,191,143,.22), transparent 55%),
        radial-gradient(900px 500px at 90% 0%, rgba(47,111,78,.12), transparent 55%),
        var(--bg);
    }
    a{color:inherit}
    .container{width:min(1120px, calc(100% - 32px)); margin:0 auto;}
    .nowrap{white-space:nowrap}

    /* ===== Header ===== */
    header{
      position:sticky;
      top:0;
      z-index:40;
      backdrop-filter: blur(10px);
      background: rgba(246,248,243,.86);
      border-bottom:1px solid var(--line);
    }
    .nav{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:14px;
      padding:14px 0;
    }
    .brand{
      display:flex; align-items:center; gap:10px;
      min-width:0;
      text-decoration:none;
    }
    .logo{
      width:40px;height:40px;border-radius:14px;
      display:grid;place-items:center;
      background: linear-gradient(180deg, var(--primary), var(--accent));
      color:#fff;
      font-weight:1000;
      letter-spacing:.2px;
      box-shadow: 0 10px 22px rgba(47,111,78,.18);
    }
    .brandText{display:flex; flex-direction:column; gap:2px; min-width:0}
    .brandText b{font-size:15px}
    .brandText span{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

    .navRight{display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:flex-end}
    .pill{
      font-size:12px;
      padding:9px 11px;
      border-radius:999px;
      border:1px solid var(--line);
      background: rgba(255,255,255,.70);
      text-decoration:none;
      color:var(--text);
    }
    .btn{
      border:0;
      cursor:pointer;
      padding:10px 14px;
      border-radius:999px;
      background: linear-gradient(180deg, var(--primary), var(--primary2));
      color:#fff;
      font-weight:900;
      box-shadow: var(--shadow2);
      display:inline-flex; align-items:center; gap:8px;
      white-space:nowrap;
    }
    .btn:active{transform: translateY(1px);}
    .btnGhost{
      background: rgba(255,255,255,.82);
      border:1px solid rgba(47,111,78,.22);
      color: var(--primary2);
      box-shadow:none;
      font-weight:900;
    }
    .btnSoft{
      background: rgba(111,191,143,.18);
      border:1px solid rgba(47,111,78,.18);
      color: var(--primary2);
      box-shadow:none;
      font-weight:900;
    }

    /* ===== Hero ===== */
    .hero{padding:44px 0 12px}
    .heroGrid{
      display:grid;
      grid-template-columns: 1.15fr .85fr;
      gap:16px;
      align-items:stretch;
    }
    .heroCard{
      background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.82));
      border:1px solid var(--line);
      border-radius: var(--r);
      box-shadow: var(--shadow);
      padding:22px;
      overflow:hidden;
      position:relative;
    }
    .heroCard:before{
      content:"";
      position:absolute;
      inset:-120px -120px auto auto;
      width:300px;height:300px;border-radius:50%;
      background: radial-gradient(circle at 40% 40%, rgba(111,191,143,.40), transparent 60%);
      pointer-events:none;
    }
    .kicker{
      display:inline-flex;
      gap:8px; align-items:center;
      padding:6px 10px;
      border-radius:999px;
      background: var(--soft);
      border:1px solid rgba(47,111,78,.15);
      color: rgba(47,111,78,.96);
      font-weight:900;
      font-size:12px;
      position:relative;
      z-index:1;
    }
    h1{
      margin:12px 0 10px;
      font-size: clamp(26px, 3.2vw, 40px);
      line-height:1.12;
      letter-spacing:-.2px;
      position:relative; z-index:1;
    }
    .lead{
      margin:0 0 16px;
      color:var(--muted);
      font-size:15px;
      line-height:1.6;
      position:relative; z-index:1;
    }
    .heroActions{
      display:flex;
      gap:10px;
      flex-wrap:wrap;
      align-items:center;
      margin-top:12px;
      position:relative; z-index:1;
    }
    .trustRow{
      display:flex; gap:12px; flex-wrap:wrap;
      margin-top:14px;
      color:var(--muted);
      font-size:12px;
      position:relative; z-index:1;
    }
    .trustRow b{color:var(--text)}
    .sideCard{
      background: linear-gradient(180deg, rgba(47,111,78,.10), rgba(255,255,255,.86));
      border:1px solid rgba(47,111,78,.16);
      border-radius: var(--r);
      box-shadow: var(--shadow);
      padding:18px;
      display:flex; flex-direction:column; gap:14px;
    }
    .miniTitle{
      font-size:14px;
      font-weight:1000;
      margin:0 0 6px;
    }
    .steps{margin:0;padding-left:18px;color:var(--muted);font-size:13px;line-height:1.55}
    .steps li{margin:6px 0}
    .badges{display:flex; flex-wrap:wrap; gap:8px}
    .badge{
      font-size:12px;
      padding:6px 10px;
      border-radius:999px;
      background: rgba(255,255,255,.72);
      border:1px solid rgba(47,111,78,.18);
      color: rgba(47,111,78,.95);
      font-weight:900;
    }

    /* ===== Sections ===== */
    section{padding:18px 0}
    .secHead{
      display:flex; justify-content:space-between; align-items:flex-end;
      gap:12px; flex-wrap:wrap;
      margin:0 0 12px;
    }
    .secHead h2{margin:0;font-size:18px}
    .secHead p{margin:0;color:var(--muted);font-size:13px}
    .grid3{display:grid; grid-template-columns: repeat(3,1fr); gap:12px}
    .grid2{display:grid; grid-template-columns: repeat(2,1fr); gap:12px}
    .card{
      background: var(--card);
      border:1px solid var(--line);
      border-radius: var(--r);
      box-shadow: 0 12px 30px rgba(17,24,39,.08);
      padding:16px;
    }
    .card b{display:block;margin-bottom:6px}
    .card p{margin:0;color:var(--muted);font-size:13px;line-height:1.55}
    .list{margin:10px 0 0; padding-left:18px; color:var(--muted); font-size:13px; line-height:1.55}
    .list li{margin:6px 0}

    /* ===== Best-seller cards ===== */
    .dealGrid{display:grid; grid-template-columns: repeat(3,1fr); gap:12px}
    .deal{
      background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.86));
      border:1px solid rgba(47,111,78,.16);
      border-radius: var(--r);
      box-shadow: 0 14px 34px rgba(47,111,78,.12);
      padding:16px;
      display:flex; flex-direction:column; gap:10px;
      position:relative;
      overflow:hidden;
    }
    .deal:before{
      content:"";
      position:absolute; inset:-60px -60px auto auto;
      width:180px;height:180px;border-radius:50%;
      background: radial-gradient(circle at 40% 40%, rgba(111,191,143,.28), transparent 62%);
      pointer-events:none;
    }
    .dealTop{display:flex; align-items:flex-start; justify-content:space-between; gap:10px; position:relative; z-index:1}
    .dealName{font-weight:1000}
    .dealTag{
      font-size:11px;
      padding:5px 9px;
      border-radius:999px;
      background: rgba(111,191,143,.18);
      border:1px solid rgba(47,111,78,.16);
      color: rgba(47,111,78,.95);
      font-weight:1000;
      white-space:nowrap;
    }
    .priceRow{display:flex; gap:10px; align-items:baseline; flex-wrap:wrap; position:relative; z-index:1}
    .price{font-weight:1100; font-size:18px; color: var(--primary2)}
    .old{color:var(--muted); text-decoration:line-through; font-size:13px}
    .dealActions{display:flex; gap:10px; flex-wrap:wrap; position:relative; z-index:1}
    .deal small{color:var(--muted); position:relative; z-index:1}

    /* ===== Social proof ===== */
    .quote{
      background: rgba(255,255,255,.92);
      border:1px solid var(--line);
      border-radius: var(--r);
      padding:14px;
      box-shadow: 0 12px 28px rgba(17,24,39,.08);
    }
    .quote p{margin:0 0 10px; color:var(--text); font-size:13px; line-height:1.55}
    .who{font-size:12px; color:var(--muted); font-weight:900}

    /* ===== FAQ ===== */
    .faq{display:grid; grid-template-columns: 1fr; gap:10px}
    details{
      background: rgba(255,255,255,.92);
      border:1px solid var(--line);
      border-radius: 16px;
      padding:12px 14px;
      box-shadow: 0 10px 22px rgba(17,24,39,.06);
    }
    summary{
      cursor:pointer;
      font-weight:1000;
      outline:none;
    }
    details p{margin:10px 0 0; color:var(--muted); font-size:13px; line-height:1.55}

    /* ===== Footer ===== */
    footer{
      padding:22px 0 120px; /* room for sticky CTA */
      color:var(--muted);
      font-size:12px;
    }
    .footRow{
      display:flex;
      justify-content:space-between;
      gap:12px;
      flex-wrap:wrap;
      border-top:1px solid var(--line);
      padding-top:16px;
    }

    /* ===== Sticky CTA bar ===== */
    .ctaBar{
      position:fixed; left:0; right:0; bottom:0;
      z-index:45;
      background: rgba(255,255,255,.92);
      border-top:1px solid var(--line);
      backdrop-filter: blur(10px);
      padding:10px 0;
      padding-bottom: max(10px, env(safe-area-inset-bottom));
    }
    .ctaInner{
      display:flex; align-items:center; justify-content:space-between; gap:10px;
    }
    .ctaLeft{
      display:flex; flex-direction:column; gap:2px; min-width:0;
    }
    .ctaLeft b{font-size:13px}
    .ctaLeft span{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .ctaBtns{display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end}

    /* ===== Chat widget ===== */
    .overlay{
      position:fixed; inset:0;
      background: rgba(17,24,39,.35);
      backdrop-filter: blur(6px);
      z-index:60;
      display:none;
      align-items:flex-end;
      justify-content:flex-end;
      padding:16px;
      padding-bottom: max(16px, env(safe-area-inset-bottom));
    }
    .overlay.show{display:flex;}
    .widget{
      width: min(440px, calc(100vw - 32px));
      height: min(660px, calc(100vh - 120px));
      border-radius: 18px;
      background: rgba(255,255,255,.96);
      border:1px solid var(--line);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
    }
    .wTop{
      display:flex; align-items:center; justify-content:space-between; gap:10px;
      padding:12px 12px;
      background: rgba(255,255,255,.96);
      border-bottom:1px solid var(--line);
    }
    .wTitle{display:flex; flex-direction:column; gap:2px; min-width:0}
    .wTitle b{font-size:13px}
    .wTitle small{font-size:12px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .statusDot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#22c55e;margin-right:6px;transform: translateY(-1px);}
    .statusDot.off{background:#ef4444;}
    .wBtns{display:flex; gap:8px; align-items:center}
    .iconBtn{
      width:34px;height:34px;border-radius:12px;
      border:1px solid var(--line);
      background: rgba(47,111,78,.06);
      cursor:pointer;
      color: var(--primary2);
    }
    .iconBtn:hover{background: rgba(47,111,78,.10);}
    .wBody{
      flex:1;
      overflow:auto;
      padding:12px;
      background: linear-gradient(180deg, rgba(238,246,240,.60), rgba(246,248,243,.60));
    }
    .msg{display:flex; margin:10px 0;}
    .msg.me{justify-content:flex-end}
    .bubble{
      max-width: 86%;
      padding:10px 12px;
      border-radius:14px;
      border:1px solid rgba(17,24,39,.10);
      background: rgba(255,255,255,.90);
      white-space:pre-wrap;
      line-height:1.45;
      font-size:14px;
    }
    .me .bubble{
      background: rgba(111,191,143,.18);
      border-color: rgba(47,111,78,.18);
    }

    .quickRow{
      display:flex; gap:8px; flex-wrap:wrap;
      margin-top:8px;
    }
    .qBtn{
      font-size:12px;
      padding:8px 10px;
      border-radius:999px;
      border:1px solid rgba(47,111,78,.18);
      background: rgba(255,255,255,.86);
      cursor:pointer;
      font-weight:900;
      color: var(--primary2);
    }
    .qBtn.primary{
      background: rgba(47,111,78,.10);
      border-color: rgba(47,111,78,.22);
    }

    .wDock{
      padding:12px;
      border-top:1px solid var(--line);
      background: rgba(255,255,255,.96);
    }
    .composer{display:flex; gap:10px; align-items:flex-end;}
    textarea{
      flex:1;
      min-height:44px;
      max-height:110px;
      resize:vertical;
      padding:10px 12px;
      border-radius:14px;
      border:1px solid rgba(17,24,39,.14);
      background: #fff;
      color: var(--text);
      outline:none;
      font-size:14px;
      line-height:1.35;
    }
    textarea::placeholder{color:rgba(107,114,128,.95)}
    .sendBtn{
      height:44px;
      padding:0 14px;
      border-radius:14px;
      border:0;
      background: linear-gradient(180deg, var(--primary), var(--primary2));
      color:#fff;
      cursor:pointer;
      font-weight:1000;
      display:flex; align-items:center; gap:8px;
      box-shadow: 0 10px 26px rgba(47,111,78,.18);
      white-space:nowrap;
    }
    .sendBtn:disabled{opacity:.65; cursor:not-allowed; box-shadow:none}
    .sub{
      margin-top:8px;
      display:flex;
      justify-content:space-between;
      gap:10px;
      flex-wrap:wrap;
      font-size:12px;
      color: var(--muted);
    }
    .sub a{color: var(--primary2); text-decoration:none; font-weight:1000}

    /* typing */
    .typing{
      display:flex; align-items:center; gap:8px;
      font-size:12px; color:var(--muted);
      padding:4px 2px 0;
    }
    .dots{display:flex; gap:4px; align-items:center}
    .dots i{
      width:6px;height:6px;border-radius:50%;
      background: rgba(107,114,128,.55);
      animation: b 1.1s infinite ease-in-out;
    }
    .dots i:nth-child(2){animation-delay:.15s}
    .dots i:nth-child(3){animation-delay:.3s}
    @keyframes b{
      0%,80%,100%{transform: translateY(0); opacity:.55}
      40%{transform: translateY(-4px); opacity:1}
    }

    /* ===== Quick order modal ===== */
    .modal{
      position:fixed; inset:0;
      background: rgba(17,24,39,.40);
      z-index:70;
      display:none;
      align-items:center;
      justify-content:center;
      padding:16px;
    }
    .modal.show{display:flex}
    .modalCard{
      width:min(520px, calc(100vw - 32px));
      background: rgba(255,255,255,.98);
      border:1px solid var(--line);
      border-radius: 18px;
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .mTop{
      padding:14px 14px;
      border-bottom:1px solid var(--line);
      display:flex; align-items:center; justify-content:space-between; gap:10px;
    }
    .mTop b{font-size:14px}
    .mBody{padding:14px}
    .mGrid{display:grid; grid-template-columns: 1fr 1fr; gap:10px}
    .field{display:flex; flex-direction:column; gap:6px}
    .field label{font-size:12px; color:var(--muted); font-weight:900}
    .field input, .field select, .field textarea{
      padding:10px 10px;
      border-radius: 14px;
      border:1px solid rgba(17,24,39,.14);
      outline:none;
      font-size:14px;
      background:#fff;
      color:var(--text);
    }
    .field textarea{min-height:84px; resize:vertical}
    .mFoot{
      padding:14px;
      border-top:1px solid var(--line);
      display:flex; gap:10px; justify-content:flex-end; flex-wrap:wrap;
      background: rgba(246,248,243,.75);
    }
    .note{
      margin-top:10px;
      font-size:12px;
      color:var(--muted);
      line-height:1.5;
    }
    .miniWarn{
      color: var(--warn);
      font-weight:1000;
    }

    /* ===== Responsive ===== */
    @media (max-width: 900px){
      .heroGrid{grid-template-columns: 1fr;}
      .dealGrid{grid-template-columns: 1fr;}
      .grid3{grid-template-columns: 1fr;}
      .grid2{grid-template-columns: 1fr;}
      .ctaInner{flex-direction:column; align-items:stretch}
      .ctaBtns{justify-content:stretch}
      .btn,.btnGhost,.btnSoft{width:100%; justify-content:center}
    }
  </style>
</head>
<body>

<script>
  // ===== DN mẫu: chỉnh nhanh tại đây (white-label) =====
  window.BRAND = {
    name: "TPCN Thiên Nhiên (DN mẫu)",
    slogan: "Tư vấn minh bạch • Dễ dùng • Kết nối CSKH nhanh",
    hotline: "0900 000 000",
    zalo: "https://zalo.me/0000000000",
    fanpage: "https://facebook.com/ten-fanpage",
    website: "https://example.com",
    policy: {
      cod: true,
      ship_days: "1–3 ngày",
      freeship: "Freeship đơn từ 500.000đ",
      return_policy: "Đổi trả trong 7 ngày nếu sản phẩm lỗi/đóng gói lỗi."
    },
    badges: ["Nguồn gốc rõ ràng", "Minh bạch thành phần", "Tư vấn theo dữ liệu", "Không hứa “khỏi bệnh”"],
    bestsellers: [
      {
        id:"combo1",
        name:"Combo Ổn định đường huyết",
        tag:"Bán chạy",
        price:"1.250.000đ",
        old:"1.410.000đ",
        benefit:"Hỗ trợ ổn định đường huyết, hỗ trợ chuyển hoá.",
        link:"https://example.com/combo01"
      },
      {
        id:"combo2",
        name:"Combo Dạ dày – Trào ngược",
        tag:"Ưu đãi",
        price:"990.000đ",
        old:"1.120.000đ",
        benefit:"Hỗ trợ tiêu hoá, giảm khó chịu vùng thượng vị.",
        link:"https://example.com/combo02"
      },
      {
        id:"combo3",
        name:"Combo Mỡ máu – Tim mạch",
        tag:"Đề xuất",
        price:"1.090.000đ",
        old:"1.240.000đ",
        benefit:"Hỗ trợ mỡ máu, hỗ trợ tim mạch.",
        link:"https://example.com/combo03"
      }
    ],
    testimonials: [
      { text:"Tư vấn rõ ràng, dễ hiểu. Mình được gợi ý combo phù hợp và hướng dẫn dùng chi tiết.", who:"C.H (HN)" },
      { text:"Giao nhanh, đóng gói cẩn thận. Hỏi COD/ship là AI trả lời rất mượt.", who:"A.T (BN)" },
      { text:"Có câu hỏi khó thì bot hướng dẫn liên hệ CSKH ngay, chuyên nghiệp.", who:"M.Q (HCM)" },
      { text:"Mình thích phần minh bạch: không hứa khỏi bệnh, chỉ nói hỗ trợ/cải thiện.", who:"L.P (ĐN)" },
      { text:"AI hỏi đúng 1–2 câu rồi tư vấn thẳng vào vấn đề, tiết kiệm thời gian.", who:"N.K (HP)" },
      { text:"Nút đặt nhanh tiện, nhập SĐT là có người gọi xác nhận liền.", who:"D.V (TH)" }
    ]
  };
</script>

<header>
  <div class="container">
    <div class="nav">
      <a class="brand" href="#top" aria-label="Trang chủ">
        <div class="logo">🌿</div>
        <div class="brandText">
          <b id="brandName">Hệ sinh thái TPCN thiên nhiên</b>
          <span id="brandSlogan">Tư vấn minh bạch • Trợ lý AI thông minh</span>
        </div>
      </a>
      <div class="navRight">
        <a class="pill" id="btnWebsite" href="#" target="_blank" rel="noopener">Website</a>
        <a class="pill" id="btnFanpage" href="#" target="_blank" rel="noopener">Fanpage</a>
        <a class="pill" id="btnZalo" href="#" target="_blank" rel="noopener">Zalo</a>
        <button class="btn" id="btnOpenTop" type="button">Tư vấn cùng AI</button>
      </div>
    </div>
  </div>
</header>

<main id="top">
  <div class="container">

    <!-- ===== HERO ===== -->
    <section class="hero">
      <div class="heroGrid">
        <div class="heroCard">
          <div class="kicker">🌱 Thiên nhiên • Minh bạch • Hỗ trợ sức khỏe</div>
          <h1 id="heroTitle">Giải pháp chăm sóc sức khỏe từ thiên nhiên<br/>dành cho gia đình Việt</h1>
          <p class="lead" id="heroLead">
            Hệ sinh thái TPCN từ nguồn gốc tự nhiên, minh bạch thông tin.
            Trợ lý AI giúp anh/chị chọn đúng sản phẩm/combo theo nhu cầu và hướng dẫn mua hàng nhanh.
          </p>

          <div class="heroActions">
            <button class="btn" id="btnOpenHero" type="button">Tư vấn cùng AI</button>
            <button class="btn btnGhost" id="btnScrollDeals" type="button">Xem combo bán chạy</button>
            <button class="btn btnSoft" id="btnOrderQuick" type="button">Đặt nhanh</button>
          </div>

          <div class="trustRow">
            <span>✅ <b>Không</b> chẩn đoán • không thay thế bác sĩ</span>
            <span>✅ Không cam kết “khỏi bệnh”</span>
            <span>✅ Tư vấn theo <b>dữ liệu sản phẩm</b></span>
          </div>
        </div>

        <div class="sideCard">
          <div>
            <div class="miniTitle">AI tư vấn & chốt đơn theo 3 bước</div>
            <ol class="steps">
              <li>Hỏi 1–2 câu để hiểu đúng nhu cầu (nếu cần).</li>
              <li>Đối chiếu dữ liệu combo/sản phẩm của doanh nghiệp.</li>
              <li>Đề xuất phương án + chốt mềm (COD/CK) hoặc kết nối CSKH.</li>
            </ol>
          </div>
          <div>
            <div class="miniTitle">Điểm tin cậy</div>
            <div class="badges" id="badges"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== BEST SELLER DEALS ===== -->
    <section id="deals">
      <div class="secHead">
        <h2>Combo bán chạy (đề xuất nhanh)</h2>
        <p>Nhấn <b>Tư vấn AI</b> để cá nhân hoá theo nhu cầu • Hoặc <b>Đặt nhanh</b> trong 30 giây</p>
      </div>

      <div class="dealGrid" id="dealGrid"></div>
    </section>

    <!-- ===== ECOSYSTEM ===== -->
    <section id="ecosystem">
      <div class="secHead">
        <h2>Hệ sinh thái sản phẩm</h2>
        <p>Nhóm công dụng phổ biến • Tư vấn combo/sản phẩm theo tình trạng và mục tiêu</p>
      </div>

      <div class="grid3">
        <div class="card"><b>🌿 Nhóm chuyển hoá</b><p>Hỗ trợ đường huyết, mỡ máu, gan… tư vấn theo thói quen sinh hoạt.</p></div>
        <div class="card"><b>🌿 Nhóm tiêu hoá</b><p>Hỗ trợ dạ dày, trào ngược, men vi sinh… gợi ý theo mức độ.</p></div>
        <div class="card"><b>🌿 Nhóm xương khớp</b><p>Hỗ trợ vận động, giảm khó chịu… gợi ý theo độ tuổi.</p></div>
        <div class="card"><b>🌿 Nhóm miễn dịch</b><p>Hỗ trợ đề kháng theo mùa, theo thể trạng… ưu tiên dễ dùng.</p></div>
        <div class="card"><b>🌿 Nhóm giấc ngủ</b><p>Hỗ trợ ngủ ngon, thư giãn… gợi ý theo lịch ngủ và stress.</p></div>
        <div class="card"><b>🌿 Nhóm làm đẹp</b><p>Hỗ trợ da/tóc… gợi ý theo mục tiêu và thời gian mong muốn.</p></div>
      </div>
    </section>

    <!-- ===== POLICIES ===== -->
    <section id="policy">
      <div class="secHead">
        <h2>Ưu đãi & chính sách mua hàng</h2>
        <p>Rõ ràng • minh bạch • hỗ trợ nhanh</p>
      </div>
      <div class="grid2">
        <div class="card">
          <b>🚚 Giao hàng & thanh toán</b>
          <ul class="list" id="policyList"></ul>
        </div>
        <div class="card">
          <b>📌 Lưu ý an toàn (TPCN)</b>
          <ul class="list">
            <li><b class="miniWarn">Không</b> chẩn đoán • không thay thế bác sĩ.</li>
            <li><b class="miniWarn">Không</b> cam kết “khỏi bệnh”, chỉ “hỗ trợ/cải thiện”.</li>
            <li>Nếu mang thai/cho con bú/trẻ em/đang dùng thuốc kê đơn: nên hỏi CSKH để tư vấn thận trọng.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ===== TRUST / CERT ===== -->
    <section id="trust">
      <div class="secHead">
        <h2>Minh bạch & uy tín</h2>
        <p>Thêm chứng nhận/kiểm định thật của DN để tăng tỷ lệ chốt</p>
      </div>
      <div class="grid3">
        <div class="card"><b>🏷️ Nguồn gốc nguyên liệu</b><p>Thông tin xuất xứ rõ ràng, minh bạch.</p></div>
        <div class="card"><b>🧪 Kiểm định chất lượng</b><p>Chỉ tiêu chất lượng/giấy tờ (DN thay bằng dữ liệu thật).</p></div>
        <div class="card"><b>🏭 Chuẩn sản xuất</b><p>GMP/ISO (nếu có) • quy trình quản lý chất lượng.</p></div>
      </div>
    </section>

    <!-- ===== SOCIAL PROOF ===== -->
    <section id="reviews">
      <div class="secHead">
        <h2>Khách hàng nói gì?</h2>
        <p>Feedback ngắn gọn • tăng độ tin cậy khi khách đang phân vân</p>
      </div>
      <div class="grid3" id="reviewGrid"></div>
    </section>

    <!-- ===== FAQ ===== -->
    <section id="faq">
      <div class="secHead">
        <h2>FAQ • Hỏi nhanh đáp gọn</h2>
        <p>Những câu hỏi ảnh hưởng trực tiếp đến quyết định mua</p>
      </div>
      <div class="faq">
        <details>
          <summary>Có COD không?</summary>
          <p id="faqCod">Có. Anh/chị có thể chọn COD khi đặt hàng.</p>
        </details>
        <details>
          <summary>Giao hàng mất bao lâu?</summary>
          <p id="faqShip">Thông thường 1–3 ngày tuỳ khu vực.</p>
        </details>
        <details>
          <summary>Freeship áp dụng thế nào?</summary>
          <p id="faqFree">Freeship đơn từ 500.000đ (tuỳ chương trình).</p>
        </details>
        <details>
          <summary>Đổi trả thế nào?</summary>
          <p id="faqReturn">Đổi trả trong 7 ngày nếu sản phẩm lỗi/đóng gói lỗi.</p>
        </details>
        <details>
          <summary>AI có thể tư vấn “khỏi bệnh” không?</summary>
          <p>Không. Trợ lý AI chỉ hỗ trợ lựa chọn sản phẩm/combo theo dữ liệu doanh nghiệp, không cam kết kết quả.</p>
        </details>
        <details>
          <summary>Khi nào cần gặp CSKH?</summary>
          <p>Nội dung kinh doanh/đại lý/hoa hồng, khiếu nại phức tạp, hoặc tình trạng cần thận trọng (mang thai, trẻ em, đang dùng thuốc kê đơn).</p>
        </details>
      </div>
    </section>

    <footer>
      <div class="footRow">
        <div>© <span id="footBrand">TPCN Thiên Nhiên (DN mẫu)</span></div>
        <div>Landing Page + AI Agent chốt đơn • minh bạch & an toàn</div>
      </div>
    </footer>

  </div>
</main>

<!-- ===== Sticky CTA ===== -->
<div class="ctaBar" role="region" aria-label="CTA">
  <div class="container">
    <div class="ctaInner">
      <div class="ctaLeft">
        <b>Muốn chốt nhanh? 👇</b>
        <span>Nhấn <b>Tư vấn AI</b> để cá nhân hoá • hoặc <b>Đặt nhanh</b> (COD/CK) trong 30 giây</span>
      </div>
      <div class="ctaBtns">
        <button class="btn" id="btnOpenCta" type="button">Tư vấn cùng AI</button>
        <button class="btn btnGhost" id="btnOrderCta" type="button">Đặt nhanh</button>
        <a class="btn btnSoft" id="btnZaloCta" href="#" target="_blank" rel="noopener">Zalo</a>
      </div>
    </div>
  </div>
</div>

<!-- ===== Chat overlay ===== -->
<div class="overlay" id="overlay" role="dialog" aria-modal="true" aria-label="AI Chat">
  <div class="widget" role="document">
    <div class="wTop">
      <div class="wTitle">
        <b>Trợ lý AI TPCN</b>
        <small><span id="dot" class="statusDot"></span><span id="status">Đang kiểm tra kết nối…</span></small>
      </div>
      <div class="wBtns">
        <button class="iconBtn" id="btnQuickOrder" title="Đặt nhanh">🛒</button>
        <button class="iconBtn" id="btnClear" title="Xoá hội thoại">🧹</button>
        <button class="iconBtn" id="btnClose" title="Đóng">✕</button>
      </div>
    </div>

    <div class="wBody" id="chat"></div>

    <div class="wDock">
      <div class="composer">
        <textarea id="txt" placeholder="Nhập câu hỏi… (VD: Đau dạ dày/trào ngược dùng combo nào?)"></textarea>
        <button class="sendBtn" id="send"><span>Gửi</span><span aria-hidden="true">➤</span></button>
      </div>
      <div class="sub">
        <span>⏎ Enter gửi • Shift+Enter xuống dòng</span>
        <span><a href="#" id="btnExample">Gợi ý câu hỏi</a></span>
      </div>
    </div>
  </div>
</div>

<!-- ===== Quick Order modal ===== -->
<div class="modal" id="modal" role="dialog" aria-modal="true" aria-label="Đặt nhanh">
  <div class="modalCard" role="document">
    <div class="mTop">
      <b>Đặt nhanh (CSKH xác nhận trong thời gian sớm)</b>
      <button class="iconBtn" id="btnModalClose" title="Đóng">✕</button>
    </div>
    <div class="mBody">
      <div class="mGrid">
        <div class="field">
          <label>Chọn combo/sản phẩm</label>
          <select id="odItem"></select>
        </div>
        <div class="field">
          <label>Hình thức thanh toán</label>
          <select id="odPay">
            <option value="COD">COD (nhận hàng trả tiền)</option>
            <option value="Chuyển khoản">Chuyển khoản</option>
          </select>
        </div>

        <div class="field">
          <label>Họ tên</label>
          <input id="odName" placeholder="VD: Nguyễn Văn A" />
        </div>
        <div class="field">
          <label>Số điện thoại *</label>
          <input id="odPhone" inputmode="tel" placeholder="VD: 09xxxxxxxx" />
        </div>

        <div class="field">
          <label>Tỉnh/Thành *</label>
          <input id="odArea" placeholder="VD: Hà Nội" />
        </div>
        <div class="field">
          <label>Ghi chú (tuỳ chọn)</label>
          <input id="odNote" placeholder="VD: giao giờ hành chính" />
        </div>
      </div>

      <div class="note">
        <b class="miniWarn">Lưu ý:</b> TPCN chỉ hỗ trợ sức khỏe, <b>không</b> chẩn đoán và không cam kết khỏi bệnh.
        Nếu anh/chị đang dùng thuốc kê đơn, mang thai/cho con bú/trẻ em… vui lòng ghi chú để CSKH tư vấn thận trọng.
      </div>
    </div>

    <div class="mFoot">
      <button class="btn btnGhost" id="btnModalCancel" type="button">Huỷ</button>
      <button class="btn" id="btnModalSubmit" type="button">Gửi đơn</button>
    </div>
  </div>
</div>

<script>
  // ===== Setup brand from window.BRAND =====
  const BRAND = window.BRAND || {};
  const API = location.origin;

  function $(id){ return document.getElementById(id); }

  $("brandName").textContent = BRAND.name || "Hệ sinh thái TPCN thiên nhiên";
  $("brandSlogan").textContent = BRAND.slogan || "Tư vấn minh bạch • Trợ lý AI thông minh";
  $("footBrand").textContent = BRAND.name || "DN mẫu";

  // links
  function safeHref(v){ return (v && String(v).startsWith("http")) ? v : "#"; }
  $("btnWebsite").href = safeHref(BRAND.website);
  $("btnFanpage").href = safeHref(BRAND.fanpage);
  $("btnZalo").href = safeHref(BRAND.zalo);
  $("btnZaloCta").href = safeHref(BRAND.zalo);

  // badges
  const badges = $("badges");
  (BRAND.badges || []).forEach(t=>{
    const s = document.createElement("span");
    s.className="badge";
    s.textContent = t;
    badges.appendChild(s);
  });

  // deals
  const dealGrid = $("dealGrid");
  const items = BRAND.bestsellers || [];
  function dealCard(d){
    const el = document.createElement("div");
    el.className = "deal";
    el.innerHTML = `
      <div class="dealTop">
        <div class="dealName">${escapeHtml(d.name || "Combo")}</div>
        <div class="dealTag">${escapeHtml(d.tag || "Hot")}</div>
      </div>
      <div class="priceRow">
        <div class="price">${escapeHtml(d.price || "")}</div>
        ${d.old ? `<div class="old">${escapeHtml(d.old)}</div>` : ``}
      </div>
      <small>${escapeHtml(d.benefit || "")}</small>
      <div class="dealActions">
        <button class="btn" type="button" data-ai="${escapeHtml(d.name||"")}" data-link="${escapeHtml(d.link||"")}">Tư vấn AI</button>
        <button class="btn btnGhost" type="button" data-order="${escapeHtml(d.name||"")}" data-pay="COD">Đặt nhanh</button>
        <a class="btn btnSoft" href="${safeHref(d.link)}" target="_blank" rel="noopener">Xem chi tiết</a>
      </div>
    `;
    return el;
  }
  items.forEach(d=> dealGrid.appendChild(dealCard(d)));

  // policy list
  const pol = BRAND.policy || {};
  const policyList = $("policyList");
  const li = (t)=>{ const x=document.createElement("li"); x.textContent=t; policyList.appendChild(x); };
  li(`Thanh toán: ${pol.cod ? "Có COD" : "Không COD"} • Có chuyển khoản.`);
  li(`Thời gian giao: ${pol.ship_days || "1–3 ngày"} (tuỳ khu vực).`);
  if (pol.freeship) li(pol.freeship);
  if (pol.return_policy) li(`Đổi trả: ${pol.return_policy}`);
  if (BRAND.hotline) li(`CSKH/Hotline: ${BRAND.hotline}`);

  // FAQ dynamic
  $("faqCod").textContent = pol.cod ? "Có. Anh/chị có thể chọn COD khi đặt hàng." : "Hiện tại chưa hỗ trợ COD, anh/chị có thể chuyển khoản khi đặt hàng.";
  $("faqShip").textContent = `Thông thường ${pol.ship_days || "1–3 ngày"} tuỳ khu vực.`;
  $("faqFree").textContent = pol.freeship || "Tuỳ chương trình tại thời điểm đặt hàng.";
  $("faqReturn").textContent = pol.return_policy || "Vui lòng liên hệ CSKH để được hỗ trợ đổi trả theo chính sách.";

  // reviews
  const reviewGrid = $("reviewGrid");
  (BRAND.testimonials || []).slice(0,6).forEach(r=>{
    const q = document.createElement("div");
    q.className = "quote";
    q.innerHTML = `<p>“${escapeHtml(r.text||"") }”</p><div class="who">— ${escapeHtml(r.who||"")}</div>`;
    reviewGrid.appendChild(q);
  });

  // scroll buttons
  $("btnScrollDeals").onclick = () => $("deals").scrollIntoView({behavior:"smooth"});

  // ===== Chat widget =====
  const overlay = $("overlay");
  const btnOpenTop = $("btnOpenTop");
  const btnOpenHero = $("btnOpenHero");
  const btnOpenCta = $("btnOpenCta");
  const btnClose = $("btnClose");
  const btnClear = $("btnClear");
  const btnExample = $("btnExample");
  const btnSend = $("send");
  const txt = $("txt");
  const chat = $("chat");
  const dot = $("dot");
  const statusEl = $("status");
  const btnQuickOrder = $("btnQuickOrder");

  function openChat(){
    overlay.classList.add("show");
    setTimeout(() => txt.focus(), 50);
    ping();
  }
  function closeChat(){ overlay.classList.remove("show"); }

  btnOpenTop.onclick = openChat;
  btnOpenHero.onclick = openChat;
  btnOpenCta.onclick = openChat;
  btnClose.onclick = closeChat;

  overlay.addEventListener("click", (e)=>{ if(e.target === overlay) closeChat(); });

  // formatting
  function escapeHtml(s){
    return String(s||"").replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  }
  function formatLite(md){
    let s = escapeHtml(String(md||""));
    s = s.replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
    s = s.replace(/\[([^\]]+?)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:#24563c;text-decoration:underline;font-weight:1000">$1</a>');
    s = s.replace(/^###\s*(.+)$/gm, "<b>$1</b>");
    s = s.replace(/\n/g, "<br>");
    return s;
  }
  function add(role, content, withQuick=false){
    const row = document.createElement("div");
    row.className = "msg " + (role === "me" ? "me" : "bot");

    const b = document.createElement("div");
    b.className = "bubble";
    b.innerHTML = formatLite(content);

    row.appendChild(b);

    if(withQuick && role !== "me"){
      const q = document.createElement("div");
      q.className = "quickRow";
      q.innerHTML = `
        <button class="qBtn primary" type="button" id="qOrder">🛒 Đặt nhanh</button>
        <a class="qBtn" href="${safeHref(BRAND.zalo)}" target="_blank" rel="noopener">💬 Zalo 1-1</a>
        <a class="qBtn" href="${safeHref(BRAND.fanpage)}" target="_blank" rel="noopener">📣 Fanpage</a>
      `;
      b.appendChild(q);

      setTimeout(()=>{
        const qOrder = row.querySelector("#qOrder");
        if(qOrder) qOrder.onclick = ()=> openOrderModal();
      }, 0);
    }

    chat.appendChild(row);
    chat.scrollTop = chat.scrollHeight;
  }

  // typing indicator (professional)
  const THINKING = [
    "Đang suy nghĩ…"
  ];
  let thinkTimer=null, thinkIdx=0;
  function showThinking(show){
    let el = document.getElementById("typing");
    if(show){
      if(el) return;
      el = document.createElement("div");
      el.id = "typing";
      el.className = "typing";
      el.innerHTML = '<span id="thinkText">'+THINKING[0]+'</span><span class="dots"><i></i><i></i><i></i></span>';
      chat.appendChild(el);
      chat.scrollTop = chat.scrollHeight;

      thinkIdx = 0;
      thinkTimer = setInterval(()=>{
        const tt = document.getElementById("thinkText");
        thinkIdx = (thinkIdx + 1) % THINKING.length;
        if(tt) tt.textContent = THINKING[thinkIdx];
      }, 1200);
    }else{
      if(thinkTimer){ clearInterval(thinkTimer); thinkTimer=null; }
      if(el) el.remove();
    }
  }

  async function ping(){
    try{
      const r = await fetch(API + "/health", {cache:"no-store"});
      const j = await r.json();
      dot.classList.remove("off");
      statusEl.textContent = "Online • " + (j.profile || "profile");
    }catch(_){
      dot.classList.add("off");
      statusEl.textContent = "Offline (không truy cập được /health)";
    }
  }

  // session id to keep agent memory
  function getSessionId(){
    const k = "tpcn_session_id";
    let v = localStorage.getItem(k);
    if(!v){
      v = "sess_" + Math.random().toString(16).slice(2) + "_" + Date.now().toString(16);
      localStorage.setItem(k, v);
    }
    return v;
  }

  async function sendMessage(m){
    m = String(m||"").trim();
    if(!m) return;
    add("me", m);
    btnSend.disabled = true;
    showThinking(true);

    try{
      const res = await fetch(API + "/chat", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ message: m, session_id: getSessionId() })
      });
      const data = await res.json();
      showThinking(false);
      add("bot", data.reply || "Dạ em chưa nhận được phản hồi hợp lệ. Anh/chị thử lại giúp em nhé ạ.", true);
    }catch(e){
      showThinking(false);
      add("bot", "Dạ hệ thống đang bận hoặc lỗi kết nối. Anh/chị thử tải lại trang giúp em nhé ạ.", true);
    }finally{
      btnSend.disabled = false;
      txt.focus();
    }
  }

  async function send(){
    const m = txt.value.trim();
    if(!m) return;
    txt.value = "";
    await sendMessage(m);
  }

  btnSend.onclick = send;
  txt.addEventListener("keydown", (e)=>{
    if(e.key === "Enter" && !e.shiftKey){
      e.preventDefault();
      send();
    }
  });

  btnClear.onclick = ()=>{
    chat.innerHTML = "";
    add("bot",
      "Dạ em chào anh/chị 😊 Em là **Trợ lý AI tư vấn TPCN thiên nhiên**. " +
      "Anh/chị đang quan tâm nhóm nào ạ (dạ dày/đường huyết/mỡ máu/gan/xương khớp/giấc ngủ…)?",
      true
    );
  };

  btnExample.onclick = (e)=>{
    e.preventDefault();
    openChat();
    txt.value = "Đau dạ dày / trào ngược thì nên dùng combo nào? Cho em cách dùng và link mua ạ.";
    txt.focus();
  };

  // open from deal cards: ask AI specifically + include link
  dealGrid.addEventListener("click", (e)=>{
    const t = e.target;
    if(!(t instanceof HTMLElement)) return;

    const ai = t.getAttribute("data-ai");
    const order = t.getAttribute("data-order");
    if(ai){
      openChat();
      const link = t.getAttribute("data-link") || "";
      const msg = `Tư vấn giúp em về **${ai}**. Em muốn biết: gồm những sản phẩm gì, cách dùng, dùng bao lâu, giá và link đặt hàng. ${link ? ("Link tham khảo: "+link) : ""}`;
      sendMessage(msg);
    }
    if(order){
      openOrderModal(order);
    }
  });

  // initial greeting
  add("bot",
    "Dạ em chào anh/chị 😊 Em là **Trợ lý AI tư vấn TPCN thiên nhiên**. " +
    "Anh/chị đang quan tâm vấn đề nào ạ (dạ dày/đường huyết/mỡ máu/gan/xương khớp/giấc ngủ…)?",
    true
  );

  // ===== Quick order modal =====
  const modal = $("modal");
  const btnModalClose = $("btnModalClose");
  const btnModalCancel = $("btnModalCancel");
  const btnModalSubmit = $("btnModalSubmit");
  const odItem = $("odItem");
  const odPay = $("odPay");
  const odName = $("odName");
  const odPhone = $("odPhone");
  const odArea = $("odArea");
  const odNote = $("odNote");

  function openOrderModal(preselectName=""){
    // populate
    odItem.innerHTML = "";
    const opts = (BRAND.bestsellers || []).map(x => x.name);
    const base = ["Tư vấn chọn giúp em (chưa chọn combo)"].concat(opts);
    base.forEach(name=>{
      const op = document.createElement("option");
      op.value = name;
      op.textContent = name;
      odItem.appendChild(op);
    });
    if(preselectName){
      odItem.value = preselectName;
    }
    modal.classList.add("show");
    setTimeout(()=> odPhone.focus(), 50);
  }
  function closeOrderModal(){ modal.classList.remove("show"); }

  $("btnOrderQuick").onclick = ()=> openOrderModal();
  $("btnOrderCta").onclick = ()=> openOrderModal();
  btnQuickOrder.onclick = ()=> openOrderModal();

  btnModalClose.onclick = closeOrderModal;
  btnModalCancel.onclick = closeOrderModal;
  modal.addEventListener("click", (e)=>{ if(e.target === modal) closeOrderModal(); });

  // validate phone loosely (VN)
  function normPhone(s){ return String(s||"").trim(); }

  btnModalSubmit.onclick = async ()=>{
    const item = odItem.value || "Chưa chọn combo";
    const pay = odPay.value || "COD";
    const name = odName.value.trim();
    const phone = normPhone(odPhone.value);
    const area = odArea.value.trim();
    const note = odNote.value.trim();

    if(!phone || phone.length < 9){
      alert("Anh/chị vui lòng nhập SĐT hợp lệ để CSKH xác nhận đơn ạ.");
      odPhone.focus();
      return;
    }
    if(!area){
      alert("Anh/chị vui lòng nhập Tỉnh/Thành để bên em tư vấn ship & giao hàng ạ.");
      odArea.focus();
      return;
    }

    closeOrderModal();
    openChat();

    // Send as a natural message so backend agent can extract slots (name/phone/area) and store lead.
    const leadMsg =
      `Em muốn **đặt hàng nhanh**. ` +
      `Sản phẩm/Combo: ${item}. ` +
      `Họ tên: ${name || "(chưa cung cấp)"}; ` +
      `SĐT: ${phone}; ` +
      `Tỉnh/Thành: ${area}; ` +
      `Thanh toán: ${pay}. ` +
      (note ? `Ghi chú: ${note}. ` : "") +
      `Nhờ CSKH xác nhận và gửi link/đơn giúp em ạ.`;

    await sendMessage(leadMsg);
  };

  // expose openChat for CTA in header (if needed externally)
  window.openChat = openChat;
  window.openOrderModal = openOrderModal;
</script>

</body>
</html>
