export const columns = [
  {
    headerName: "Name",
    field: "name"
  },
  {
    headerName: "Type",
    field: "type",
    flex: 1
  },
  {
    headerName: "Component",
    field: "component_name",
    flex: 1
  },
  {
    headerName: "Aggregations",
    field: "aggregations",
    flex: 1,
    valueGetter: (params) => (Array.isArray(params.data.aggregations) ? params.data.aggregations.join(", ") : "")
  },
  {
    headerName: "Created",
    field: "created_at",
    flex: 1,
    valueFormatter: (params) => (params.value ? new Date(params.value).toLocaleString() : "")
  }
];
