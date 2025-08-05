$(document).ready(function() {
  $('#id_paciente, #id_doctor').select2({
    ajax: {
      url: function() {
        if (this[0].id === 'id_paciente') {
          return '/citas/api/buscar_pacientes/';
        } else {
          return '/citas/api/buscar_doctores/';
        }
      },
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return {
          q: params.term, // search term
          page: params.page || 1
        };
      },
      processResults: function(data, params) {
        params.page = params.page || 1;
        return {
          results: data.results,
          pagination: {
            more: data.has_next
          }
        };
      },
      cache: true
    },
    minimumInputLength: 1,
    width: '100%',
    placeholder: 'Buscar...',
    allowClear: true,
    maximumSelectionLength: 1
  });
});
