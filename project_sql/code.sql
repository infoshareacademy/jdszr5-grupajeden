-- Table: Income by actor per month

create table income_by_actor_per_month as
	select
		a.actor_id
		, concat (a.last_name
			, ' '
			, a.first_name) as actor
		, sum(amount) as income
		, count(distinct f.film_id) as film_amount
		, sum(amount) / count(distinct f.film_id) as income_per_film
		, (sum(amount) / count(distinct f.film_id)) / 
			count(distinct concat(date_part('year', rental_date)::varchar, date_part('month', rental_date))::varchar) 
			as avg_income_per_film_per_month
		, dense_rank () over (
			order by (sum(amount) / count(distinct f.film_id)) / 
			count(distinct concat(date_part('year', rental_date)::varchar, date_part('month', rental_date))::varchar)) 
			as ranking_per_film_per_income_per_month
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
		avg_income_per_film_per_month
;

-- Table: Income per actor per month

create table income_per_actor_per_month as
	select
		a.actor_id
		, concat (a.last_name
			, ' '
			, a.first_name) as actor
		, date_part('year', r.rental_date) year_number
		, date_part('month', r.rental_date) month_number
		, sum(amount) as income_per_actor
		, count(distinct f.film_id) as film_ammount
		, sum(amount) / count(distinct f.film_id) as income_per_film
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
		, date_part('year', r.rental_date)
		, date_part('month', r.rental_date)
;

-- Table: Popularity by actor per appereances

create table popularity_by_actor_per_appereances as 
		with actor_num as 
			(
			select
				a.actor_id
				, concat (a.last_name
					, ' '
					, a.first_name) as actor
				, count(f.film_id) as number_of_appereances
			from
				actor a
			join film_actor fa on
				a.actor_id = fa.actor_id
			join film f on
				fa.film_id = f.film_id
			group by
				actor
				, a.actor_id
			order by
				number_of_appereances asc
			)
	select
		*
		, dense_rank() over (
		order by number_of_appereances desc)
	from
		actor_num
;

-- Correlation: Number of appereances / Income per film per month

select
	corr(popularity_by_actor_per_appereances.number_of_appereances, 
		income_by_actor_per_month.avg_income_per_film_per_month)
from
	income_by_actor_per_month
join popularity_by_actor_per_appereances on
	income_by_actor_per_month.actor_id = popularity_by_actor_per_appereances.actor_id
;

-- Correlation: Income per actor / Income per film

select
	corr(income_per_actor, income_per_film)
from
	income_per_actor_per_month ipapm
;

-- Additional statistic functions regarding popularity

select
	mode() within group (
	order by number_of_appereances) mode_appereances
	, percentile_disc(0.1) within group (
	order by number_of_appereances) perc01_appereances
	, percentile_disc(0.5) within group (
	order by number_of_appereances) perc05_appereances
	, percentile_disc(0.9) within group (
	order by number_of_appereances) perc09_appereances
	, stddev(number_of_appereances) stddev_appereances
	, variance(number_of_appereances) variance_appereances
from
	popularity_by_actor_per_appereances
;

-- Additional statistic functions regarding income

select
	mode() within group (
	order by income_per_actor) mode_income
	, percentile_disc(0.1) within group (
	order by income_per_actor) perc01_income
	, percentile_disc(0.5) within group (
	order by income_per_actor) perc05_income
	, percentile_disc(0.9) within group (
	order by income_per_actor) perc09_income
	, stddev(income_per_actor) stddev_income
	, variance(income_per_actor) variance_income
from
	income_per_actor_per_month ipapm
;

-- Table: Ranking over categories

create table ranking_over_categories as
	select
		c."name" as category_name
		, count (r.rental_id)*sum(p.amount) as final_sum
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
		final_sum desc
;

-- Correlation: Ranking over categories

select
	corr(ibapm.avg_income_per_film_per_month, roc.final_sum)
from
	income_by_actor_per_month ibapm
join film_actor fa on
	ibapm.actor_id = fa.actor_id
join film f on
	fa.film_id = f.film_id
join film_category fc on
	f.film_id = fc.category_id
join category c on
	fc.category_id = c.category_id
join ranking_over_categories roc on
	c."name" = roc.category_name
;

-- Table: Ranking over ratings

create table ranking_over_ratings as
	select
		f.rating
		, count (r.rental_id)*sum(p.amount) as final_sum
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
		final_sum desc
;
	
-- Correlation: Ranking over ratings

select
	corr(ibapm.avg_income_per_film_per_month, ror.final_sum)
from
	income_by_actor_per_month ibapm
join film_actor fa on
	ibapm.actor_id = fa.actor_id
join film f on
	fa.film_id = f.film_id
join ranking_over_ratings ror on
	f.rating = ror.rating
;

-- Table: Actors and films

create table act_film as
	select
		a.actor_id
		, concat(a.last_name
			, ' '
			, a.first_name) as full_name
		, fa.film_id
	from
		actor a
	join film_actor fa on
		a.actor_id = fa.actor_id
;

-- Table: Stores and cities

create table store_city as
	select
		s.store_id
		, c.city
	from
		store s
	join address adr on
		s.address_id = adr.address_id
	join city c on
		adr.city_id = c.city_id
;


-- Table: Rentals, payments and stores

create table pay_rent_store as
	select
		i.film_id
		, count(r.rental_id) as frequency_of_rentals
		, sum(p.amount) as sum_of_payment
		, sc.city as city_of_store
	from
		inventory i
	join rental r on
		i.inventory_id = r.inventory_id
	join payment p on
		r.rental_id = p.rental_id
	join store_city sc on
		i.store_id = sc.store_id
	group by
		i.film_id
		, sc.city
	order by
		film_id
;

-- Table: Rentals and payments

create table pay_rent as
	select
		i.film_id
		, count(r.rental_id) as frequency_of_rentals
		, sum(p.amount) as sum_of_payment
	from
		inventory i
	join rental r on
		i.inventory_id = r.inventory_id
	join payment p on
		r.rental_id = p.rental_id
	join store_city sc on
		i.store_id = sc.store_id
	group by
		i.film_id
	order by
		film_id
;

-- Table: Refunds

create table cat_film as
	select
		f.film_id
		, f.title
		, f.release_year
		, sum(f.rental_rate) * pr.frequency_of_rentals as sum_of_rental
		, f.rating
		, c."name"
		, pr.frequency_of_rentals
		, pr.sum_of_payment
		, (sum(f.rental_rate) * pr.frequency_of_rentals) - pr.sum_of_payment as refund
	from
		film f
	join film_category fc on
		f.film_id = fc.film_id
	join category c on
		fc.category_id = c.category_id
	join pay_rent pr on
		pr.film_id = f.film_id
	group by
		f.film_id
		, pr.frequency_of_rentals
		, pr.sum_of_payment
		, c."name"
;