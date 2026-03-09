from pathlib import Path
import time
import shutil


from taturtle import autocrop
from taturtle.template_matching import (
    init_templatematching,
    run_template_matching,
    save_shift_image,
    unpack_result_template_step1,
    template_median,
)
from taturtle.thickness_correction import run_thickness_correction
from taturtle.utils import arguments_parser, get_file_list


def main():
    args = arguments_parser()
    input_path = args.img_ref.parent
    output_base = args.output if args.output else input_path.parent

    # Output Paths
    (output_base / "output").mkdir(parents=True, exist_ok=True)
    (output_base / "thickness_corr").mkdir(parents=True, exist_ok=True)
    (output_base / "cropped").mkdir(parents=True, exist_ok=True)

    start = time.time()

    # Extract coordinates
    if args.region:
        row_range = [args.region[0], args.region[1]]
        col_range = [args.region[2], args.region[3]]
    else:
        row_range = args.rows if args.rows else [0, 0]
        col_range = args.cols if args.cols else [0, 0]

    #  first template matching
    if not args.crop:
        print("autocrop skipped")
        image_ref = args.img_ref
    else:
        x_shift, y_shift = autocrop.run_autocrop(
            input_path, args.img_ref, output_base / "cropped"
        )
        # x_shift is top margin (rows), y_shift is left margin (cols)
        row_range = [r - x_shift for r in row_range]
        col_range = [c - y_shift for c in col_range]
        input_path = output_base / "cropped"
        image_ref = input_path / args.img_ref.name

    if not args.thick_corr:
        template = init_templatematching(
            input_path, image_ref, row_range, col_range
        )
        patch_prev, prev_x, prev_y, patch_list = unpack_result_template_step1(
            run_template_matching(
                input_path,
                template,
                args.alpha,
                args.search_window,
                args.cpu,
            ),
            template.patch_ref,
            len(template.tiff_files),
        )
        results2 = run_template_matching(
            input_path,
            template_median(template, patch_list),
            args.alpha,
            args.search_window // 4,
            args.cpu,
        )
        for i, (pos_x2, pos_y2, patch_temp2) in enumerate(results2):
            shift_x, shift_y = save_shift_image(
                input_path,
                output_base / "output",
                template.tiff_files[i],
                template.init_x,
                template.init_y,
                pos_x2,
                pos_y2,
            )
            print(
                f"Registration displacement ({i + 1}/{len(template.tiff_files)}): {shift_x} - {shift_y}"
            )
        print(
            "The time of execution of the template matching without thickness correction is :",
            (time.time() - start),
            "s using",
            args.cpu,
            "CPU",
        )
    else:
        len_input_files, len_slices = run_thickness_correction(
            input_path, args.slice_thickness_nm, output_base / "thickness_corr"
        )
        print(
            "Before",
            len_input_files,
            "After",
            len_slices,
            "Thickness correction passed",
        )
        input_path = output_base / "thickness_corr"
        image_ref = input_path / f"{args.img_ref.stem}_0.tif"
        if not image_ref.exists():
            # Fallback to first file if _0 doesn't exist for some reason
            files = sorted(get_file_list(input_path))
            if files:
                image_ref = files[0]

        template = init_templatematching(input_path, image_ref, row_range, col_range)
        patch_prev, prev_x, prev_y, patch_list = unpack_result_template_step1(
            run_template_matching(
                input_path,
                template,
                args.alpha,
                args.search_window,
                args.cpu,
            ),
            template.patch_ref,
            len(template.tiff_files),
        )
        results2 = run_template_matching(
            input_path,
            template_median(template, patch_list),
            args.alpha,
            args.search_window,
            args.cpu,
        )
        for i, (pos_x2, pos_y2, patch_temp2) in enumerate(results2):
            shift_x2, shift_y2 = save_shift_image(
                input_path,
                output_base / "output",
                template.tiff_files[i],
                template.init_x,
                template.init_y,
                pos_x2,
                pos_y2,
            )
            print(
                f"Registration displacement ({i + 1}/{len(template.tiff_files)}): {shift_x2} - {shift_y2}"
            )
        print(
            "The time of execution of the template matching with thickness correction is :",
            (time.time() - start),
            "s using",
            args.cpu,
            "CPU",
        )

    # Cleanup: Move files from "output" to output_base and remove subfolders
    output_dir = output_base / "output"
    if output_dir.exists():
        for f in output_dir.iterdir():
            if f.is_file():
                dest = output_base / f.name
                if dest.exists():
                    dest.unlink()
                shutil.move(str(f), str(dest))
        output_dir.rmdir()

    for subfolder in ["cropped", "thickness_corr"]:
        path = output_base / subfolder
        if path.exists():
            shutil.rmtree(path)


if __name__ == "__main__":
    main()
