-- Table: Income by actor per month:

create table income_by_actor_per_month as
select
	a.actor_id,
	concat (a.last_name,
	' ',
	a.first_name) as actor ,
	sum(amount) as income,
	count(distinct f.film_id) as film_amount,
	sum(amount) / count(distinct f.film_id) as income_per_film ,
	(sum(amount) / count(distinct f.film_id)) / count(distinct concat(date_part('year', rental_date)::varchar, date_part('month', rental_date))::varchar) as avg_income_per_film_per_month,
	dense_rank () over (
order by
	(sum(amount) / count(distinct f.film_id)) / count(distinct concat(date_part('year', rental_date)::varchar, date_part('month', rental_date))::varchar)) as ranking_per_film_per_income_per_month
from
	actor a
join film_actor fa on
	fa.actor_id = a.actor_id
join film f on
	f.film_id = fa.film_id
join inventory i on
	i.film_id = f.film_id
join rental r on
	r.inventory_id = i.inventory_id
join payment p on
	p.rental_id = r.rental_id
group by
	a.actor_id
order by
	avg_income_per_film_per_month;

-- Table: Income per actor per month:

create table income_per_actor_per_month as
select
	a.actor_id,
	concat (a.last_name,
	' ',
	a.first_name) as actor,
	date_part('year', r.rental_date) year_number,
	date_part('month', r.rental_date) month_number,
	sum(amount) as income_per_actor,
	count(distinct f.film_id) as film_ammount,
	sum(amount) / count(distinct f.film_id) as income_per_film
from
	actor a
join film_actor fa on
	fa.actor_id = a.actor_id
join film f on
	f.film_id = fa.film_id
join inventory i on
	i.film_id = f.film_id
join rental r on
	r.inventory_id = i.inventory_id
join payment p on
	p.rental_id = r.rental_id
group by
	a.actor_id,
	date_part('year', r.rental_date),
	date_part('month', r.rental_date);

-- Table: Popularity by actor per appereances:

create table popularity_by_actor_per_appereances as with actor_num as(
select
	a.actor_id,
	concat (a.last_name,
	' ',
	a.first_name) as actor,
	count(f.film_id)::numeric as number_of_appereances
from
	actor a
join film_actor fa on
	a.actor_id = fa.actor_id
join film f on
	fa.film_id = f.film_id
group by
	actor,
	a.actor_id
order by
	number_of_appereances asc )
select
	*,
	dense_rank() over (
order by
	number_of_appereances desc)
from
	actor_num;

-- Correlation [to_be_changed]:

select
	corr(popularity_by_actor_per_appereances.number_of_appereances, income_by_actor_per_month.avg_income_per_film_per_month)
from
	income_by_actor_per_month
join popularity_by_actor_per_appereances on
	income_by_actor_per_month.actor_id = popularity_by_actor_per_appereances.actor_id;

-- Additional statistic functions regarding popularity:

select
	mode() within group (
order by
	number_of_appereances) mode_appereances,
	percentile_disc(0.1) within group (
order by
	number_of_appereances) perc01_appereances,
	percentile_disc(0.5) within group (
order by
	number_of_appereances) perc05_appereances,
	percentile_disc(0.9) within group (
order by
	number_of_appereances) perc09_appereances
from
	popularity_by_actor_per_appereances;

-- Additional statistic functions regarding income:

select
	mode() within group (
order by
	income_per_film) mode_income,
	percentile_disc(0.1) within group (
order by
	income_per_film) perc01_income,
	percentile_disc(0.5) within group (
order by
	income_per_film) perc05_income,
	percentile_disc(0.9) within group (
order by
	income_per_film) perc09_income
from
	income_by_actor_per_month ibapm;

-- Ranking over categories:

select
	c."name" as category_name,
	count (r.rental_id)* sum(p.amount)::numeric as final_sum
from
	film f
join film_category fc on
	f.film_id = fc.film_id
join category c on
	fc.category_id = c.category_id
join film_actor fa on
	f.film_id = fa.film_id
join actor a on
	fa.actor_id = a.actor_id
join inventory i on
	f.film_id = i.film_id
join rental r on
	i.inventory_id = r.inventory_id
join payment p on
	r.rental_id = p.rental_id
group by
	category_name
order by
	final_sum desc;

-- Ranking over ratings:

select
	f.rating,
	count (r.rental_id)* sum(p.amount)::numeric as final_sum
from
	film f
join film_category fc on
	f.film_id = fc.film_id
join category c on
	fc.category_id = c.category_id
join film_actor fa on
	f.film_id = fa.film_id
join actor a on
	fa.actor_id = a.actor_id
join inventory i on
	f.film_id = i.film_id
join rental r on
	i.inventory_id = r.inventory_id
join payment p on
	r.rental_id = p.rental_id
group by
	f.rating
order by
	final_sum desc;