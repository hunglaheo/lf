const map = L.map('map').setView([10.8715825, 106.7432922], 15);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const LeafIcon = L.Icon.extend({
	options: {
		iconSize:     [46, 23],
		popupAnchor:  [-3, -10]
	}
});

const greenIcon = new LeafIcon({iconUrl: '/static/car-green.png'});
const redIcon = new LeafIcon({iconUrl: '/static/car-red.png'});

// Khởi tạo mảng markers
const markers = [];

let filters = [];

let table;

// Hàm lấy dữ liệu
async function fetchData() {
  const response = await $.get("http://lfgps.khaanh.com:8080/GetListVehicleForMap/"+auth_code);
  return response;
	
  //const response = await fetch('./truck.json');
  //return await response.json();
}

const listTruck = []

// Hàm tạo các marker ban đầu 
async function createMarkers(callback) {
  const cars = await fetchData();
  
  var html = '';
  cars.forEach(car => {
	if(car[6]!==null && car[7]!==null){
		const carId = car[1];
		
		//Nếu car10 = 2 thì không hiện
		if (!markers[carId] && car[10] < 2) {
			markers[carId] = {};
			markers[carId].id = carId;
			markers[carId].coords = [car[6], car[7]]; 
			
			var trang_thai = car[9] == 'Dừng chạy' ? 'car-stop' : 'car-start';
			
			let hours = parseInt(car[5] / 3600);
			let minutes = parseInt(car[5] % 3600 / 60);
			
			if(hours < 10)
				hours = "0"+hours;
			if(minutes < 10)
				minutes = "0"+minutes;
			
			html += '<tr id="'+carId+'" class="'+trang_thai+'"><td>'+car[8]+'</td><td>'+car[2]+'</td><td>'+car[3]+'</td><td>'+carId+'</td><td>'+car[4]+'</td><td>'+hours+":"+minutes+'</td><td>'+car[11].replace('T',' ')+'</td></tr>';
			
			markers[carId].map = L.marker([car[6], car[7]], {
				icon: car[9] == 'Dừng chạy' ? redIcon : greenIcon,
				iconAnchor: [car[6], car[7]]
			}).bindTooltip("<span><span class='tooltip-soxe'>" + carId + "</span><span class='tooltip-show'>"+ car[2] +"   "+ car[4]+"</span></span>", {direction:'top',permanent:true,offset:[0,-10]}).addTo(map).openTooltip();
			//}).bindTooltip("<span class='tooltip-soxe'>" + carId + "</span>", {direction:'top',permanent:false,offset:[0,-10]}).addTo(map).openTooltip().bindPopup("<span class='tooltip-soxe'>" + carId + "</span><br>"+ car[2] +"   "+ car[4], {direction:'bottom',offset:[0,10]}); //<br>" + car[2] +"   "+ car[4]
			markers[carId].map.on('click', function(e) {
				const marker = e.target;
				const tooltip = marker.getTooltip();

				if (tooltip) {
					const content = tooltip.getContent();
					const newContent = content.includes('tooltip-hide')
						? content.replaceAll('tooltip-hide', 'tooltip-show')
						: content.replaceAll('tooltip-show', 'tooltip-hide');
					tooltip.setContent(newContent);
					tooltip.update();
				}
			});
		}else if(markers[carId]){
			//add them tooltip vao markers[carId]
			let marker = markers[carId].map;
			
			var currentTooltip = marker.getTooltip();
			
			if (currentTooltip) {
			  var tooltipContent = currentTooltip.getContent();
			}else{
				var tooltipContent = '';
			}
			
			let newTooltip = tooltipContent.replace("</span></span>","<br>"+car[2] +"   "+ car[4]+"</span></span>");
			
			marker.bindTooltip(newTooltip, {
				direction: 'top',
				offset: [0,-10],
				permanent:true
			}).openTooltip();
			
			/*var currentPopup = marker.getPopup();
			
			if (currentPopup) {
			  var popupContent = currentPopup.getContent();
			}else{
				var popupContent = '';
			}
			
			let newPopup = popupContent+"<br>"+car[2] +"   "+ car[4];
			
			marker.bindPopup(newPopup, {
				direction: 'bottom',
				offset: [0,10]
			});*/
		}
	}
  });
  document.getElementById('car-list-row').innerHTML = html;
  
  callback();
}

// Hàm cập nhật marker
async function updateMarkers() {
	const cars = await fetchData();
	// Lấy dữ liệu mới
	cars.forEach(car => {
		if(car[6]!==null && car[7]!==null){
			const carId = car[1];
			const newCoords = [car[6], car[7]];
			if(markers[carId]){
				if(car[10] == 2){
					markers[carId].map.setOpacity(0);
					$('#'+carId).hide();
				}else{
					markers[carId].map.setOpacity(1);
					$('#'+carId).show();
					markers[carId].map.setLatLng(newCoords);
				}
				
				if(car[9]=="Dừng chạy"){
					markers[carId].map.setIcon(redIcon);
					$('#'+carId).addClass('car-stop');
					$('#'+carId).removeClass('car-start');
					//$('#'+carId+' td:nth-child(7)').html('Dừng chạy');
				}else{
					markers[carId].map.setIcon(greenIcon);
					$('#'+carId).addClass('car-start');
					$('#'+carId).removeClass('car-stop');
					//$('#'+carId+' td:nth-child(7)').html('Đang chạy');
				}
				
				$('#'+carId+' td:nth-child(7)').html(car[11].replace('T',' '));
			}
		}
	});
	filterRows();
}

function addClickEvents() {
	Object.keys(markers).forEach(id => {
		const marker = markers[id];
		
		document.getElementById(id).addEventListener('click', () => {
			const coords = marker.map.getLatLng();
			map.flyTo(coords, 16);
		});
	});
}

// Gọi các hàm
createMarkers(() => {
  addClickEvents();
  table = $('#car-table').DataTable({
            orderCellsTop: true,
			"paging": false,
            initComplete: function () {
            var api = this.api();
            count = 0;
            $('.filterhead', api.table().header()).each( function (i) {
                var column = api.column(i);
                var title = column.header();
                //replace spaces with dashes
                titleid = $(title).html().replace(/[\W]/g, '-');
                
                var select = $('<select id="' + titleid + '" class="select2" ></select>')
                    .appendTo( $(this).empty() )
                    .on( 'change', function () {
                      //Get the "text" property from each selected data 
                      //regex escape the value and store in array
                      var data = $.map( $(this).select2('data'), function( value, key ) {
                        return value.text ? '^' + $.fn.dataTable.util.escapeRegex(value.text) + '$' : null;
                                 });
                      
                      //if no data selected use ""
                      if (data.length === 0) {
                        data = [""];
                      }
                      
                      //join array into string with regex or (|)
                      var val = data.join('|');
                      
                      //search for the option(s) selected
                      column
                            .search( val ? val : '', true, false )
                            .draw();
					  filterRows();
                    } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.append( '<option value="'+d+'">'+d+'</option>' );
                } );
              
              //use column title as selector and placeholder
              $('#' + titleid).select2({
                multiple: true,
                closeOnSelect: false,
                placeholder: "Chọn " + $(title).html()
              });
              
              //initially clear select otherwise first option is selected
              $('.select2').val(null).trigger('change');
            } );
        },
		"responsive": true, "lengthChange": false, "autoWidth": false, "aaSorting": []
  });
});

// Cập nhật sau 30s
setInterval(updateMarkers, 30000);

function filterRows() {
	filters = [];
	$('#car-table tr').each(function() {
		var id = $(this).attr('id');
		if(id){
			filters.push(id);
		}
	});
  
	Object.keys(markers).forEach(id => {
		if (!filters.includes(id)) {
			markers[id].map.setOpacity(0);
			markers[id].map.getTooltip().setOpacity(0);
		}else{
			markers[id].map.setOpacity(1);
			markers[id].map.getTooltip().setOpacity(0.9);
		}
	});
}

const distributorIcon = L.icon({
  iconUrl: '/static/distribution-center.png',
  iconSize: [35, 35], 
  popupAnchor: [-3, -10]
});

const distMarkers = [];

async function loadDistributors() {

  const distributors = await getDistributors();

  distributors.forEach(d => {
    const marker = L.marker([d[3], d[4]], {
      icon: distributorIcon
    }).bindTooltip(d[2], {direction:'bottom',permanent:true,offset:[0,20]}).addTo(map).openTooltip();
	
	distMarkers.push(marker);
  });

}

async function getDistributors() {

  // code call API
  try {
    const response = await fetch("http://lfgps.khaanh.com:8080/ListNPP");
    const data = await response.json();
    return data;

  } catch (error) {
    console.log(error);
  }

}

loadDistributors();

let clickCount = 0;
$('.offnpp').on('click', function() {
  if (distMarkers.length > 0) {
    clickCount++;
    if (clickCount === 1) {
      // Ẩn tooltip
      distMarkers.forEach(marker => {  
        marker.getTooltip().setOpacity(0);
      });
    } else if(clickCount === 2) {
      // Ẩn cả marker và tooltip
      distMarkers.forEach(marker => {
        marker.setOpacity(0);
        marker.getTooltip().setOpacity(0);
      });
    } else if(clickCount === 3) { 
      // Show lại cả marker và tooltip
      distMarkers.forEach(marker => {
        marker.setOpacity(1);
        marker.getTooltip().setOpacity(0.9); 
      });
      clickCount = 0; // Reset lại clickCount
    }
  }
});

$('.offtrucks').on('click', function() {
	Object.keys(markers).forEach(id => {
		const tooltip = markers[id].map.getTooltip();

		if (tooltip) {
			const content = tooltip.getContent();
			const newContent = content.includes('tooltip-hide')
				? content.replaceAll('tooltip-hide', 'tooltip-show')
				: content.replaceAll('tooltip-show', 'tooltip-hide');
			tooltip.setContent(newContent);
			tooltip.update();
		}
	});
});