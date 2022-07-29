/*Manages data save POST calls*/

function saveData(data, metadata, sensitive){
  var full_data = JSON.parse(data);
  var metadata = JSON.parse(metadata);
  full_data.unshift({"Participant": `${metadata["Participant"]}`, 'Gen': `${metadata["Gen"]}`, 'Sensitive': sensitive});
  data = JSON.stringify(full_data);
  fetch(`${metadata["URL"]}`, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: data
  })
}

function saveDataNoIter(data, id, url, sensitive){
  full_data = JSON.parse(data)
  full_data.unshift({'ID': id, 'Sensitive': sensitive})
  data = JSON.stringify(full_data)
  fetch(url, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: data
  })
}