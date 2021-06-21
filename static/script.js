function encode(obj) {
  return btoa(unescape(encodeURIComponent(JSON.stringify(obj))));
}

function decode(str) {
  return JSON.parse(decodeURIComponent(escape(atob(str))));
}

function url() {
  let flagbox = document.getElementById("flags");
  var items = [code.value, stdin.value, flagbox.value, [...$(".argbox>textarea")].map(x => x.value)];
  return "/#" + encode(items);
}

function format() {
  let flagbox = document.getElementById("flags");
  return "# [yuno]" + (flagbox.value.trim() == "" ? "" : " `" + flagbox.value.trim() + "`") + ", " + code.value.length + " byte" + (code.value.length == 1 ? "" : "s") + "\n\n```\n" + code.value + "\n```\n\n[Try it online!](" + document.location + " \"yuno online interpreter\")\n\n[yuno]: https://github.com/hyper-neutrino/yuno";
}

let FLAGS = {
  "L": "forcelist",
  "T": "capten",
  "U": "ir_upper",
  "D": "ir_lower",
  "O": "ir_outer",
  "I": "ir_inner",
  "h": "help",
  "j": "ioj_newline",
  "k": "ioj_space",
  "t": "round_thousandth"
};

function execute_code() {
  let flagbox = document.getElementById("flags");
  outlabel.innerHTML = "STDOUT";
  var input = prompt;
  if (!$("#promptinstead").is(":checked")) {
    var lines = stdin.value.split("\n");
    lines.reverse();
    input = (a => () => a.pop())(lines);
  }
  output.value = "";
  stderr.value = "";
  var flags = {};
  for (var x of Object.keys(FLAGS)) {
    flags[FLAGS[x]] = flagbox.value.indexOf(x) != -1;
  }
  execute(code.value, [...$(".argbox>textarea")].map(x => x.value), input, x => output.value += x, x => stderr.value += x, flags);
  updateHeight(output);
}

var counter = 0;
function add_argument(target, value) {
  counter++;
  var field = $("<textarea id='argitem" + counter + "' class='args input'>");
  if (value) {
    field.prop("value", value);
  }
  var addbutton = $("<span onclick='add_argument(\"#argbox" + counter + "\")' class='addbutton'>").html("+ add");
  var rmbutton = $("<span onclick='rm_argument(\"#argbox" + counter + "\")' class='rmbutton'>").html("- remove");
  var box = $("<div id='argbox" + counter + "' class='argbox'>");
  box.append(addbutton);
  box.append(rmbutton);
  box.append($("<br>"));
  box.append(field);
  box.append($("<br>"));
  box.append($("<br>"));
  box.insertBefore(target);
}

function rm_argument(target) {
  $(target).remove();
}

updatehistory = {}

function updateHeight(element) {
  if (updatehistory[element.id] == element.value) return;
  updatehistory[element.id] = element.value;
  element.style.height = "";
  element.style.height = element.scrollHeight + "px";
}

$(document).ready(e => {
  $(".wrap").on("keydown", e => e.ctrlKey && e.keyCode != 86 || e.metaKey || e.keyCode == 9 ? "" : e.preventDefault()).on("paste", e => e.preventDefault()).on("cut", e => e.preventDefault());
  const code = document.getElementById("code");
  const stdin = document.getElementById("stdin");
  const outlabel = document.getElementById("outlabel");
  const output = document.getElementById("output");
  const stderr = document.getElementById("stderr");
  const flagbox = document.getElementById("flags");
  const run = document.getElementById("run");

  if (document.location.hash) {
    var values = decode(document.location.hash.substring(1));
    code.value = values[0];
    stdin.value = values[1];
    flagbox.value = values[2];
    for (var x of values[3]) {
      add_argument("#base", x);
    }
    output.value = format();
  }

  u = () => {
    [...$(".input")].forEach(x => updateHeight(x));
    requestAnimationFrame(u);
  };
  requestAnimationFrame(u);

  $(document).on("keydown", e => {
    if (e.ctrlKey && e.keyCode == 13) {
      e.preventDefault();
      execute_code();
    }
  });

  $("#run").on("click", e => {
    execute_code();
  })

  $("#link").on("click", e => {
    document.location = url();
    outlabel.innerHTML = "Stack Exchange post format";
    output.value = format();
    updateHeight(output);
  });

  $("#inline").on("click", e => {
    document.location = url();
    outlabel.innerHTML = "Inline markdown format";
    output.value = "[Try it online!](" + document.location + ")";
  });
});
