/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/

select c.name, count(f.film_id) film_count
from public.film f
join public.film_category fc on f.film_id =fc.film_id
join public.category c on c.category_id =fc.category_id 
group by c.name
order by 2 desc

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/

select first_name, last_name, count(fa.film_id) rental_film_count
from public.rental r
join public.inventory i on i.inventory_id =r.inventory_id 
join public.film_actor fa on fa.film_id=i.film_id 
join public.actor a on a.actor_id =fa.actor_id 
group by first_name, last_name
order by count(fa.film_id) desc
limit 10



/*
3.
Вивести категорія фільмів, на яку було витрачено найбільше грошей
в прокаті
*/

REFRESH MATERIALIZED view public.rental_by_category
select *
from public.rental_by_category
order by 1 desc
limit 1


/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/
select f.title
from public.film f
left join (select distinct film_id
			from public.inventory) i on i.film_id =f.film_id 
where i.film_id is null

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/
select first_name, last_name, count(f.film_id) num_of_films
from public.film f
join public.film_category fc on f.film_id =fc.film_id
join public.category c on c.category_id =fc.category_id 
join public.film_actor fa on fa.film_id =f.film_id 
join public.actor a on a.actor_id =fa.actor_id 
where c.name='Children'
group by first_name, last_name
order by 3 desc
limit 3
