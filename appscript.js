function updateDataToAPI() {

  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Transport-Booking sheet');

  // Lấy ngày tại cell L1
  var bookingDate = Utilities.formatDate(getBookingDate(), "GMT+7", "yyyy-MM-dd");

  // Lấy ngày hiện tại
  var today = Utilities.formatDate(new Date(), "GMT+7", "yyyy-MM-dd");

  // Kiểm tra ngày có trùng khớp hay không
  if(bookingDate == today) {

    // Lấy vị trí dòng cuối cùng
    var lastRow = sheet.getLastRow();

    var data = [];

    // Vòng lặp từ dòng 4 đến dòng cuối cùng
    for (var i = 4; i <= lastRow; i++) {

      // Lấy dữ liệu từng dòng
      var rowData = sheet.getRange(i, 1, 1, 27).getValues()[0];
	  
      if(rowData[1] != ''){
        if(rowData[2] != '' && rowData[17].length >= 7){
          var dataItem = {};
          dataItem.lot_bien_so_xe = rowData[17];
          dataItem.lot_nha_phan_phoi = rowData[1];
          dataItem.lot_nha_van_tai = rowData[2];
          dataItem.lot_ngay_di = today;

          var date = new Date(rowData[23]);
          date.setHours(date.getHours() % 12);
          date.setTime(date.getTime() + 420000);
          dataItem.lot_gio_di = Utilities.formatDate(date, "GMT+7", "HH:mm");

          if(rowData[24] == ''){
            dataItem.lot_gio_vao = '00:00';
          }else{
            var gio_vao = new Date(rowData[24]);
            gio_vao.setHours(gio_vao.getHours() % 12);
            gio_vao.setTime(gio_vao.getTime() + 420000);
            dataItem.lot_gio_vao = Utilities.formatDate(gio_vao, "GMT+7", "HH:mm");
          }

          data.push(dataItem);
        }		  
      }else{
        break;
      }
    }

    // Gọi API để cập nhật dữ liệu
    var url = "http://lfgps.khaanh.com:8080/insert"; // URL API

    var options = {
      method: "post",
      contentType: "application/json",
      payload: JSON.stringify(data)
    };

    UrlFetchApp.fetch(url, options);
  }
}

function getBookingDate() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Huong dan su dung');
  var bookingDate = sheet.getRange('D5').getValue();

  if(bookingDate=='#NUM!'){
    var today = new Date();
    bookingDate = new Date(today.setDate(today.getDate() + 1));
  }
  
  return bookingDate;
}

function createTimeTriggerEveryNMinutes() {
  var triggers = ScriptApp.getProjectTriggers();
  var shouldCreateTrigger = true;
  triggers.forEach(function (trigger) {
    if(trigger.getHandlerFunction() === "updateDataToAPI") {
      shouldCreateTrigger = false;
    }
  });

  if(shouldCreateTrigger) {
    ScriptApp.newTrigger("updateDataToAPI")
    .timeBased()
    .everyMinutes(30)
    .create();

    updateDataToAPI();
  }
}
