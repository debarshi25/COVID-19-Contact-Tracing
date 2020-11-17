const url = 'process.php'
$(document).ready(function() {
    $(document).on('submit', '#contact_graph_form', function() {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if(xhr.readyState === XMLHttpRequest.DONE) {
                var contact_graph = '' + xhr.response
                contact_graph = contact_graph.replace(/\\n/g, '\n')
                contact_graph = contact_graph.replace(/"/g, '')
                console.log(contact_graph)

                var link = document.createElement('a')
                link.download = 'contact_graph.txt'

                var blob = new Blob([contact_graph], {type: 'text/plain'});
                link.href = window.URL.createObjectURL(blob);
                link.click()
            }
        }
        xhr.send(JSON.stringify({
            "id": $("#ID")[0].value,
            "date": $("#date")[0].value
        }));
      return false;
     });
});
