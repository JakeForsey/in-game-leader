from ingameleader.model.dao import Map, Strategy, Location, ExemplarRoute, RouteToLocation, create_session
from ingameleader.seed import MAPS, STRATEGIES, LOCATIONS, EXEMPLAR_ROUTES


def create_route_to_locations_mapping(routes):
    route_to_locations = []
    route_id = 0
    for route in routes:
        route["id"] = route_id
        route_id += 1
        for location_id in route["_locations"]:

            route_to_locations.append(
                {
                    "route_id": route["id"],
                    "location_id": location_id
                }
            )

    return route_to_locations


def main():
    with create_session() as session:
        session.bulk_insert_mappings(
            Map,
            MAPS
        )
        session.commit()
        session.bulk_insert_mappings(
            Location,
            LOCATIONS
        )
        session.commit()
        session.bulk_insert_mappings(
            Strategy,
            STRATEGIES
        )
        session.commit()
        session.bulk_insert_mappings(
            RouteToLocation,
            create_route_to_locations_mapping(EXEMPLAR_ROUTES)
        )
        session.commit()
        session.bulk_insert_mappings(
            ExemplarRoute,
            EXEMPLAR_ROUTES
        )
        session.commit()


if __name__ == "__main__":
    main()
