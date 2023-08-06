# Orbiteer

A tool to control time-range based scripts, programs, and more.

# Goals

1. Provide a consistent, elegant way of running a script repeatedly with varied inputs in a useful way, such as fitting a goal run-time.
2. Provide clear error handling and notification, failing gracefully.
3. Be highly configurable.
4. Be highly tested.


# Wanted Features

#### Legend:

| Symbol | Meaning |
|--------|---------|
| :white_check_mark: | Merged |
| :yellow_square: | In progress |
| :red_square: | Not yet begun |

### Input Generation:
- :white_check_mark: Datetime range
  - :white_check_mark: Old -> New
  - :white_check_mark: New -> Old
- :red_square: Iterate over item chunks
  - :red_square: In presented order
  - :red_square: Sorted

### Target Measurement
- :white_check_mark: Direct time taken by command
- :white_check_mark: Number returned by command

### Optimization Strategy
- :white_check_mark: Direct ratio
  - :white_check_mark: With damping
- :red_square: PID

### Targets
- :white_check_mark: Run command line
  - :white_check_mark: Args at end of command string
  - :red_square: Command line formatting
- :white_check_mark: Python Callable
- :red_square: Call URL
  - :red_square: Via request parameters
  - :red_square: Via request body
- :red_square: Append to file

### Failure retries
- :white_check_mark: Quit
- :red_square: N retries (before quit)
  - :red_square: Immediately
  - :red_square: Timed wait
  - :red_square: Exponential backoff
- :red_square: Skip
  - :red_square: Retry pattern and then skip
  - :red_square: Skip and retry again at end of run

### Notification methods
- :yellow_square: Logs
- :red_square: User-named scripts
- :red_square: [PushOver](https://pushover.net/)

### Notification events
- :yellow_square: Nominal completion
- :yellow_square: Erroring out
- :red_square: N% completion
- :red_square: Time passed


# Development

## Setup
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Run `./scripts/setup.sh`

## Check lint & formatting
```
make lint
```

## Fix formatting
```
make format
```

## Run tests & view coverage
```
make test
```

## Check lint & run tests
```
make
```
