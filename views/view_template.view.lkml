view: superstore {
  sql_table_name: Your_Schema.Your_Table ;;
  suggestions: no

  dimension: category {
    type: string
    sql: ${TABLE}.category ;;
  }
  dimension: city {
    type: string
    sql: ${TABLE}.city ;;
  }
  dimension: country {
    type: string
    map_layer_name: countries
    sql: ${TABLE}.country ;;
  }
  dimension: customer_id {
    type: string
    sql: ${TABLE}.customer_id ;;
  }
  dimension: customer_name {
    type: string
    sql: ${TABLE}.customer_name ;;
  }
  dimension: discount {
    type: string
    sql: ${TABLE}.discount ;;
  }
  dimension: order_id {
    type: string
    sql: ${TABLE}.order_id ;;
  }
  dimension: postal_code {
    type: string
    sql: ${TABLE}.postal_code ;;
  }
  dimension: product_id {
    type: string
    sql: ${TABLE}.product_id ;;
  }
  dimension: product_name {
    type: string
    sql: ${TABLE}.product_name ;;
  }
  dimension: quantity {
    type: string
    sql: ${TABLE}.quantity ;;
  }
  dimension: region {
    type: string
    sql: ${TABLE}.region ;;
  }
  dimension: row_id {
    type: string
    sql: ${TABLE}.row_id ;;
  }

  dimension: segment {
    type: string
    sql: ${TABLE}.segment ;;
  }
  dimension: ship_date {
    type: string
    sql: ${TABLE}.ship_date ;;
  }
  dimension: ship_mode {
    type: string
    sql: ${TABLE}.ship_mode ;;
  }
  dimension: state {
    type: string
    sql: ${TABLE}.state ;;
  }
  dimension: subcategory {
    type: string
    sql: ${TABLE}.subcategory ;;
  }

  dimension_group: order_date {
    type: time
    timeframes: [
      raw,
      date,
      week,
      month,
      quarter,
      year
    ]
    convert_tz: no
    datatype: date
    sql: cast(replace(order_date,'.','-') as date) ;;
  }


  measure: sales {
    type: number
    sql: sum(${TABLE}.sales) ;;
    value_format: "$#.00;-$#.00"
  }

  measure: profit {
    type: number
    sql: sum(${TABLE}.profit) ;;
    value_format: "$#.00;-$#.00"
  }


  measure: count {
    type: count
    drill_fields: [customer_name, product_name]
  }
}
