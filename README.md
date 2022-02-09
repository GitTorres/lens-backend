<!-- @format -->

# Backend server to post and get model summaries for further analysis

- `make up` to run the dev container

- `make up_prod` to run the prod container

- `make up_deploy` to run the prod container (as though you're on production server)

- `make down` to stop the container and prune orphans

- `make rebuild` to shut down running app, rebuild app image, restart app

- `make build` to construct the dev image

- `make build_prod` to construct the prod image

- `make test_utils` to run pytest suite for utility functions

- `make test_put` to run pytest suite for put endpoint for model summaries

- `make remove` to removes all related images and shuts down all related containers
