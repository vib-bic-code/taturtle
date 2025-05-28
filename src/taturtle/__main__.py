from pathlib import Path
import time


from taturtle import autocrop
from taturtle.template_matching import (
    init_templatematching,
    run_template_matching,
    save_shift_image,
    unpack_result_template_step1,
    template_median,
)
from taturtle.thickness_correction import run_thickness_correction
from taturtle.utils import arguments_parser


def main():
    args = arguments_parser()
    input_path = args.img_ref.parent

    # Output Paths
    (input_path.parent / "output").mkdir(parents=True, exist_ok=True)
    (input_path.parent / "thickness_corr").mkdir(parents=True, exist_ok=True)
    (input_path.parent / "cropped").mkdir(parents=True, exist_ok=True)

    start = time.time()

    #  first template matching
    if not args.crop:
        print("autocrop skipped")
    else:
        x_shift, y_shift = autocrop.run_autocrop(
            input_path, args.image_ref, Path("cropped")
        )
        x_a = [x - x_shift for x in args.x_a]
        y_a = [y - y_shift for y in args.y_a]
        input_path = Path(input_path).parent / "cropped"
        image_ref = input_path.parent / "cropped" / args.img_ref.name

    if not args.thick_corr:
        template = init_templatematching(input_path, image_ref, x_a, y_a, 1)
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
                "output",
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
            input_path, args.slice_thickness_nm
        )
        print(
            "Before",
            len_input_files,
            "After",
            len_slices,
            "Thickness correction passed",
        )
        template = init_templatematching(input_path, image_ref, x_a, y_a, 2)
        patch_prev, prev_x, prev_y, patch_list = unpack_result_template_step1(
            run_template_matching(
                input_path,
                template,
                args.alpha,
                args.search_window,
                args.cpu,
            ),
            template.patch_ref,
            template.tiff_files,
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
                "output",
                template.tiff_files[i],
                template.init_x,
                template.init_y,
                pos_x2,
                pos_y2,
            )
            print(
                f"Registration displacement ({i + 1}/{len(template.tiff_file)}): {shift_x2} - {shift_y2}"
            )
        print(
            "The time of execution of the template matching with thickness correction is :",
            (time.time() - start),
            "s using",
            args.cpu,
            "CPU",
        )


if __name__ == "__main__":
    main()
