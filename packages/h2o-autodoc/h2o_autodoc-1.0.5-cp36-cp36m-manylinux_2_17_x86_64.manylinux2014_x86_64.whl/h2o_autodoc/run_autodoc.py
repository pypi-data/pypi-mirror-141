import argparse
import json
import sys

from h2o_autodoc import __version__, Config, render_autodoc

VERSION = __version__


def get_dataset(h2o, dataset_key):
    if dataset_key is None:
        return None
    return h2o.get_frame(dataset_key)


def run_autodoc(
    h2o_url,
    steam_config_str,
    model_key,
    train_key,
    valid_key,
    test_key,
    additional_test_keys,
    alternative_model_keys,
    config_str,
):
    """Render h2o-autoDoc using keys - MAIN FUNCTION

    :param h2o_url: str: h2o url
    :param steam_config_str: str: h2o steam config dict as str in json format
    :param model_key: str: model key
    :param train_key: str: train dataset key
    :param valid_key: optional: str: validation dataset key
    :param test_key: optional: str: test dataset key
    :param additional_test_keys: optional: list[str]: list of additional
        test dataset keys
    :param alternative_model_keys: optional: list[str]: list of model keys of
        alternative models
    :param config_str: str: Config.serialize() output - configuration
    :return:
    """
    import h2o

    # Redirect the standard output to the standard error output
    # so that everything is logged into stderr which could be redirected
    # to a file. This includes H2O cluster status info which is printed after
    # h2o.connect/h2o.init
    stdout = sys.stdout
    sys.stdout = sys.stderr
    if steam_config_str:
        try:
            steam_config = json.loads(steam_config_str)
            h2o.connect(config=steam_config)
        except Exception as e:
            msg = (
                "Failed to connect to h2o using steam configuration: \n'{}'"
                "\nWith exception {}"
            ).format(steam_config_str, str(e))
            raise ValueError(msg)
    elif h2o_url:
        try:
            h2o.init(h2o_url)
        except Exception as e:
            msg = "Failed to connect to h2o url: '{}' with exception {}"
            msg = msg.format(h2o_url, str(e))
            raise ValueError(msg)
    else:
        raise ValueError(
            "Provide either h2o connection url or h2o steam "
            "config as string in valid json format"
        )
    # Sets the proper standard output so that if the user sets Config parameter
    # output_path=None the output report docx/zip file can be dumped to
    # the standard output and redirected to a file - useful for steam
    sys.stdout = stdout

    model = h2o.get_model(model_key)
    train = get_dataset(h2o, train_key)
    valid = get_dataset(h2o, valid_key)
    test = get_dataset(h2o, test_key)
    additional_test_sets = [get_dataset(h2o, x) for x in additional_test_keys]
    alternative_models = [h2o.get_model(key) for key in alternative_model_keys]
    config = Config(**json.loads(config_str))
    render_autodoc(
        h2o=h2o,
        config=config,
        model=model,
        train=train,
        valid=valid,
        test=test,
        additional_testsets=additional_test_sets,
        alternative_models=alternative_models,
    )
    # Redirect the standard output to the standard error output
    # so that 'H2O session closed' message is not printed to the standard
    # output which would corrupt the docx/zip file
    sys.stdout = sys.stderr


def get_key(x):
    if x is not None:
        return x.frame_id
    return None


def render_autodoc_using_keys(
    h2o, steam_config, config, model, train, valid, test, alternative_models
):
    """This function is an example of how to parse raw h2o frames/models to
    inputs required by run_autodoc

    :param h2o: optional: imported h2o (connected)
    :param steam_config: dict: optional: steam h2o cluster config dict
    :param config: Config: H2O AutoDoc Config object
    :param model: H2OModel: model
    :param train: H2OFrame: train dataset
    :param valid: optional: H2OFrame: validation dataset
    :param test: optional: H2OFrame: test dataset
    :param alternative_models: list[H2OModel]: list of alternative models
    :return:
    """
    import h2o

    if steam_config:
        steam_config = json.dumps(steam_config)
        h2o_url = None
    else:
        steam_config = None
        h2o_url = h2o.connection().base_url

    run_autodoc(
        h2o_url,
        steam_config,
        model.model_id,
        get_key(train),
        get_key(valid),
        get_key(test),
        [x.model_id for x in alternative_models],
        config.serialize(),
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Run H2O AutoDoc.\nSpecify at lease one of the following "
            "arguments: (--h2o h2o_url| --h2o-conf h2o_config_json_str)"
        )
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="H2O AutoDoc version details: %s" % VERSION,
    )
    parser.add_argument(
        "--output",
        type=str,
        help=(
            "output path (optional), "
            "result will be returned in stdout if not set"
        ),
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--h2o", type=str, help="h2o url")
    group.add_argument("--h2o-conf", type=str, help="h2o steam configuration")
    parser.add_argument("--model", type=str, required=True, help="model key")
    parser.add_argument("--train", type=str, help="train key (optional)")
    parser.add_argument("--valid", type=str, help="validation key (optional)")
    parser.add_argument(
        "--test", help="list of test keys (optional)", nargs="*"
    )
    parser.add_argument("--progress", type=str, help="progress file (optional)")

    parser.add_argument(
        "--alternative",
        type=str,
        nargs="*",
        default=[],
        help="alternative model keys (optional)",
    )

    parser.add_argument(
        "--conf", type=str, help="config settings in json string (optional)"
    )

    args = parser.parse_args()
    conf = args.conf
    if conf is not None:
        try:
            conf = json.loads(conf)
            conf["output_path"] = args.output
            conf["progress_file_path"] = args.progress
            config = Config(**conf)
        except Exception as e:
            print("Failed to load config: \n", conf)
            config = Config(
                output_path=args.output, progress_file_path=args.progress
            )
    else:
        config = Config(
            output_path=args.output, progress_file_path=args.progress
        )

    config_str = config.serialize()

    test = None
    additional_testsets = []
    if args.test:
        test = args.test[0]
        additional_testsets = args.test[1:]

    run_autodoc(
        args.h2o,
        args.h2o_conf,
        args.model,
        args.train,
        args.valid,
        test,
        additional_testsets,
        args.alternative,
        config_str,
    )


if __name__ == "__main__":
    main()
