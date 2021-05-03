$(function() {
    $('#dataTable').DataTable({
        "paging": false,
        "info": false
    });
});

$('thead th').each(function(column) {
    $(this).addClass('sortable').click(function() {
        var findSortKey = function($cell) {
            var sk = $cell.find('.sort-key').text().toUpperCase() + ' ' + $cell.text().toUpperCase();
            var ik = parseInt(sk, 10);
            return ik != NaN ? ik : sk;
        };
        var sortDirection = $(this).is('.sorted-asc') ? -1 : 1;
        //step back up the tree and get the rows with data
        //for sorting
        var $rows = $(this).parent().parent().parent().find('tbody tr').get();
        //loop through all the rows and find 
        $.each($rows, function(index, row) {
            row.sortKey = findSortKey($(row).children('td').eq(column));
        });
        //compare and sort the rows alphabetically
        $rows.sort(function(a, b) {
            if (a.sortKey < b.sortKey) return -sortDirection;
            if (a.sortKey > b.sortKey) return sortDirection;
            return 0;
        });
        //add the rows in the correct order to the bottom of the table
        $.each($rows, function(index, row) {
            $('tbody').append(row);
            row.sortKey = null;
        });
        //identify the column sort order
        $('th').removeClass('sorted-asc sorted-desc');
        var $sortHead = $('th').filter(':nth-child(' + (column + 1) + ')');
        sortDirection == 1 ? $sortHead.addClass('sorted-asc') : $sortHead.addClass('sorted-desc');
        //identify the column to be sorted by
        $('td').removeClass('sorted')
            .filter(':nth-child(' + (column + 1) + ')')
            .addClass('sorted');
    });
});


//merge rows
$(".rowEditData").click(function(index) {
    //highlight clicked row
    if (this.className.indexOf("mergeSelect") != -1) {
        this.className = this.oldClassName;
    } else {
        addClass(this, "mergeSelect");
    }
});

//add selected class to row when clicked
function addClass(element, value) {
    if (!element.className) {
        element.className = value;
    } else {
        newClassName = element.className;
        newClassName += " ";
        newClassName += value;
        element.className = newClassName;
    }
} //end addClass

$("#mergeRows").click(function() {
    var tr = document.getElementsByTagName('tr');
    var merge = tr.className.indexOf('mergeSelect');
    if (merge == -1) {
        var mergeRows = $(this);
    }
    console.log(merge);
});