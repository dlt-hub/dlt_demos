{{ config(materialized="table") }}


select *
from {{ source("pokemon_data", "pokemon") }}
limit
    1000
