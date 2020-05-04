$('input:checkbox').click(function () {
  const root = $(this).closest('div');
  const label = $(this).closest('label');

  if ($(this).prop('checked')) {
    label.removeClass(['btn-light', 'focus']);
    label.addClass('btn-success');
  } else {
    label.removeClass(['btn-success', 'focus']);
    label.addClass('btn-light');
  }

  root.find('input').not(this).prop('checked', false);
  root.find('label').not(label).removeClass(['btn-success', 'active']);
  root.find('label').not(label).addClass('btn-light');
});

$('button:reset').click(function () {
  const root = $(this).closest('form');

  root.find('input').prop('checked', false);
  root.find('label').removeClass(['btn-success', 'active']);
  root.find('label').addClass('btn-light');
});
