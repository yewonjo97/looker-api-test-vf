connection: "Your_Connection"

# include all the views
include: "/views/**/*.view.lkml"

datagroup: Your_Connection_default_datagroup {
  # sql_trigger: SELECT MAX(id) FROM etl_log;;
  max_cache_age: "1 hour"
}

persist_with: Your_Connection_default_datagroup

explore: superstore {}
