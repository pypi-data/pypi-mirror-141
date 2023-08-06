let extDiv = document.createElement("div");
let hitsUl = document.createElement("ul");
let tagsUl = document.createElement("ul");
document.body.appendChild(extDiv);
extDiv.style = "position: fixed; right: 10px; bottom: 10px; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px; min-width: 100px; min-height: 100px; max-width: 300px; max-height: 300px; border: solid #141E27 1px; background: white; overflow-wrap: break-word; overflow-y: auto; z-index: 10"
let sim_btn = document.createElement("button");
let btn_style = "margin: 10px; border: none; background: none;"
sim_btn.style = btn_style;
sim_btn.textContent = "Get Similar";
extDiv.appendChild(sim_btn);
let conc_btn = document.createElement("button");
conc_btn.style = btn_style;
conc_btn.textContent = "Get relevant tags";
extDiv.appendChild(conc_btn);
extDiv.appendChild(hitsUl);
extDiv.appendChild(tagsUl);
let curr_id = window.location.href.split("/").splice(-1)[0];

function editorOpen()
{
  return !editorDiv.classList.contains("hidden");
}
function addText(text) {
  let open = editorOpen();
  if (open)
  {
    editor.codemirror.replaceSelection(text + " ");
  }
  else {
    editor.codemirror.replaceRange("\n\n", text, {line: Infinity});
    contentDiv.innerHTML += window.parser.customRender(text);
    saveDoc();
  }

}
sim_btn.onclick = async function() {
  tagsUl.innerHTML = "";
  hitsUl.innerHTML = "";
  let req = await fetch(`/espial/semantic_search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      q: editor.value(),
      top_n: 20
    })
  });
  let results = await req.json();
  results.forEach((hit) => {
    if (hit.id != curr_id) {
      let li = document.createElement("li");  
      let a = document.createElement("a");
      li.appendChild(a);
      a.textContent = hit.title;
      a.href = `/dataobj/${hit.id}`;
      hitsUl.appendChild(li);
      let btn = document.createElement("button");
      btn.textContent = "Add Link";
    btn.style = btn_style;
    btn.style.margin = "2px";
      btn.onclick = () => {
      addText(`[[${hit.title}|${hit.id}]]`);
      }
      hitsUl.appendChild(btn);
    }
  })
}


conc_btn.onclick = async function() {
  tagsUl.innerHTML = "";
  hitsUl.innerHTML = "";
  let req = await fetch(`/espial/potential_concepts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: editor.value()
    })
  });
  let results = await req.json();
  results.forEach((hit) => {
    let li = document.createElement("li");  
    let a = document.createElement("a");
    li.appendChild(a);
    a.textContent = hit;
    a.href = `/tags/${hit}`;
    tagsUl.appendChild(li);
    let btn = document.createElement("button");
  btn.style = btn_style;
  btn.style.margin = "2px";
    btn.textContent = "Add Link";
    btn.onclick = () => {
    addText(`#${hit}#`);
    }
  li.appendChild(btn);
  })
}
