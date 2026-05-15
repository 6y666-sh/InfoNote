// static/js/main.js

document.addEventListener("DOMContentLoaded", () => {
  // ── 문제 행 클릭 → 상세 페이지 이동 ──────────
  document.querySelectorAll(".q-row[data-href]").forEach((row) => {
    row.addEventListener("click", (e) => {
      // 별표 버튼 클릭은 행 이동 제외
      if (e.target.closest(".star-btn")) return;
      window.location.href = row.dataset.href;
    });
  });

  // ── 별표 토글 (AJAX) ─────────────────────────
  document.querySelectorAll(".star-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const qid = btn.dataset.id;
      fetch(`/question/${qid}/star`, { method: "POST" })
        .then((r) => r.json())
        .then((data) => {
          btn.textContent = data.is_starred ? "★" : "☆";
          btn.classList.toggle("starred", data.is_starred);
        });
    });
  });

  // ── 이미지 미리보기 ───────────────────────────
  const imgInput = document.getElementById("image-input");
  const imgPreview = document.getElementById("image-preview");
  if (imgInput && imgPreview) {
    imgInput.addEventListener("change", () => {
      const file = imgInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          imgPreview.src = e.target.result;
          imgPreview.style.display = "block";
        };
        reader.readAsDataURL(file);
      } else {
        imgPreview.style.display = "none";
      }
    });
  }

  // ── 태그 입력 Enter키 → 쉼표로 구분 ─────────
  const tagInput = document.getElementById("tag-input");
  if (tagInput) {
    tagInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        const val = tagInput.value.trim();
        if (val && !val.endsWith(",")) {
          tagInput.value = val + ", ";
        }
      }
    });
  }
});
