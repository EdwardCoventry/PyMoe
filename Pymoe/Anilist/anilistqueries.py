
id_only_base = """
			pageInfo {
				total
				currentPage
				lastPage
				hasNextPage
			}
			media (type: ANIME) {
				id
				}
"""



#	query ($id: Int) {{

id_only_2 = """
	query ($query: {}, $page: Int, $perpage: Int) {{
		Page (page: $page, perPage: $perpage) {{
		
			pageInfo {{
				total
				currentPage
				lastPage
				hasNextPage
			}}
			media (type: ANIME) {{
				id
				}}

		}}
	}}
"""

id_only = """
	query ($query: String, $page: Int, $perpage: Int) {{
		Page (page: $page, perPage: $perpage) {{
		
		{}

		}}
	}}
""".format(id_only_base)

id_only_listings = """
	query ($page: Int, $perpage: Int) {{
		Page (page: $page, perPage: $perpage) {{
		
			pageInfo {{
				total
				currentPage
				lastPage
				hasNextPage
			}}
			media (type: ANIME, sort: {}) {{
				id
				}}

		}}
	}}
"""

full_info = """\
	query ($query: String, $page: Int, $perpage: Int) {
		Page (page: $page, perPage: $perpage) {
			pageInfo {
				total
				currentPage
				lastPage
				hasNextPage
			}
			media (anilist_search: $query, type: ANIME) {
				id
				title {
					romaji
					english
					native
				}
				# coverImage {
				#	 large
				# }
				synonyms
				averageScore
				popularity
				favourites
				genres
				episodes
				duration
				season
				hashtag
				isAdult
				format
				status
				startDate {
					year
					month
					day
					}

				relations {
					edges {
						relationType
						node {
							id
							format

						}
					}
				}

				# streamingEpisodes{
				# name
				# }

			}
		}
	}
"""

useful_base = """
			id
			idMal
			title {
				romaji
				native
				english
			}
			startDate {
				year
				month
				day
				}
			endDate {
				year
				month
				day
			}
			format
			episodes
			duration
			status
			isAdult
			averageScore
			popularity
			favourites
			
			updatedAt
			
			nextAiringEpisode {
				airingAt
				episode
				}
			
			coverImage {
				extraLarge
				large
				medium
			}
			
			relations {
				edges {
					relationType
					node {
						id
						format

					}
				}
			}

"""


# """
# 	query ($query: String, $page: Int, $perpage: Int) {
# 		Page (page: $page, perPage: $perpage) {
# """

useful_info_single = """\
	query ($query: String) {{
		Media (anilist_search: $query, type: ANIME) {{

		{}

		}}
	}}
""".format(useful_base)


page_set_up = """\
	query ($query: String, $page: Int, $perpage: Int) {{
		Page (page: $page, perPage: $perpage) {{
		

		
			media (anilist_search: $query, type: ANIME) {{
	
			{}
	
			}}
		}}
	}}
"""

useful_info = page_set_up.format(useful_base)

ids_only_3 = page_set_up.format('id')

id_useful_info = """
	query ($id: Int) {{
		Media(id: $id, type: ANIME) {{
		
		{}
		
		}}
	}}
""".format(useful_base)

get_query = """\
	query ($id: Int) {
		Media(id: $id, type: ANIME, sort: TITLE_ROMAJI) {
			id
			title {
				romaji
				english
			}
			startDate {
				year
				month
				day
			}
			endDate {
				year
				month
				day
			}
			coverImage {
				large
			}
			bannerImage
			format
			status
			episodes
			season
			description
			averageScore
			popularity
			meanScore
			genres
			synonyms
			isAdult
			nextAiringEpisode {
				airingAt
				timeUntilAiring
				episode
			}

			relations {
				edges {
					relationType
					node {
						id
						title {
							romaji
							english
							native
							# ...
						}
						synonyms
						episodes
						season
						format
						status
						startDate {
							year
							month
							day
							}
					}
				}
			}


		}
	}
"""