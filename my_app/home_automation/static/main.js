function actionLampe(){
	
	let request = new XMLHttpRequest;
	request.open('GET', "http://192.168.1.52/led");
	request.send();
	console.log("request sended...")
}


function executeAtInterval(){
	
	setInterval(function refreshData(){
		const connections = document.getElementsByClassName("connection-light")
		const datas = document.getElementsByClassName("card-text")
		
		let request = new XMLHttpRequest;
		request.open('GET', "/refresh");
		request.send();
		request.onreadystatechange = function(){
		if((this.readyState == 4) && (this.status == 200)){
			let response = JSON.parse(request.responseText);
			console.log(response);
			

			for (let i = 0; i<datas.length; i++){
				const dataEmitterID = datas[i].id.split(":")[0];
				const dataSensorID = datas[i].id.split(":")[1];
				console.log(response["datas"][dataEmitterID][1][dataSensorID]["value"]);
				if (response["datas"][dataEmitterID][1][dataSensorID]["value"] != undefined){
					document.getElementById(""+datas[i].id).innerHTML = response["datas"][dataEmitterID][1][dataSensorID]["value"];	
				}else {
					document.getElementById(""+datas[i].id).innerHTML = "waiting for data";
				} 
				

}
			for(let i = 0; i <connections.length; i++){
				const emitterID = connections[i].id.split("_")[1]
				let last_reception = new Date(response["datas"][emitterID][2]);
				console.log(last_reception)
				let now = new Date(Date.now());
				
				console.log(((now.getTime() - last_reception)/1000))
				
				
				

				if (((now.getTime() - last_reception.getTime())/1000) < 70){
					const id = "connection_" + emitterID
					document.getElementById(id).classList.remove('text-danger');
					document.getElementById(id).classList.add('text-success');


				}else{
					const id = "connection_" + emitterID
					document.getElementById(id).classList.remove('text-success');	
					document.getElementById(id).classList.add('text-danger');

				}
				
			}	
						
		}
	}
		
}, 3000);

}




