function endsWith(str, suffix) {
  return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function goBack(message = "") {
  if (message != "") {
    window.location.replace(message);
  } else {
    window.history.back();
  }
}

function collectionHas(a, b) {
  for (var i = 0, len = a.length; i < len; i++) {
    if (a[i] == b) return true;
  }
  return false;
}
function findParentBySelector(elm, selector) {
  var all = document.querySelectorAll(selector);
  var cur = elm.parentNode;
  while (cur && !collectionHas(all, cur)) {
    cur = cur.parentNode;
  }
  return cur;
}

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function renderFormErrorAfterElement(div, message) {
  let error_node = document.createElement("div");
  error_node.className = "alert alert-danger mb-1 p-2";
  error_node.setAttribute("role", "alert");
  error_node.innerHTML = message;
  insertAfter(div, error_node);
}
