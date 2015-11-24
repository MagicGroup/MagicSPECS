#!/bin/bash
# Copyright 2013 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

where=`pwd`

generated_files=`./process_ffmpeg_gyp.py $1`
generated_files_headers="${generated_files//.c/.h}"
generated_files_headers="${generated_files_headers//.S/.h}"
generated_files_headers="${generated_files_headers//.asm/.h}"

cd $1

header_files="  libavutil/x86/asm.h \
		libavutil/x86/bswap.h \
		libavutil/x86/cpu.h \
		libavutil/x86/emms.h \
		libavutil/x86/intmath.h \
		libavutil/x86/intreadwrite.h \
		libavutil/x86/timer.h \
		libavutil/atomic_gcc.h \
		libavutil/attributes.h \
		libavutil/audio_fifo.h \
		libavutil/avassert.h \
		libavutil/avutil.h \
		libavutil/bswap.h \
		libavutil/buffer_internal.h \
		libavutil/common.h \
		libavutil/colorspace.h \
		libavutil/cpu_internal.h \
		libavutil/cpu.h \
		libavutil/dynarray.h \
		libavutil/internal.h \
		libavutil/intfloat.h \
		libavutil/intreadwrite.h \
		libavutil/libm.h \
		libavutil/lls.h \
		libavutil/lzo.h \
		libavutil/macros.h \
		libavutil/old_pix_fmts.h \
		libavutil/pixfmt.h \
		libavutil/replaygain.h \
		libavutil/softfloat_tables.h \
		libavutil/thread.h \
		libavutil/timer.h \
		libavutil/timestamp.h \
		libavutil/time_internal.h \
		libavutil/version.h \
		libavutil/x86_cpu.h
		libavcodec/x86/constants.h \
		libavcodec/x86/dsputil_x86.h \
		libavcodec/x86/fft.h \
		libavcodec/x86/fpel.h \
		libavcodec/x86/hpeldsp.h \
		libavcodec/x86/inline_asm.h \
		libavcodec/x86/mathops.h \
		libavcodec/x86/vp56_arith.h \
		libavcodec/avcodec.h \
		libavcodec/blockdsp.h \
		libavcodec/bytestream.h \
		libavcodec/dct.h \
		libavcodec/dsputil.h \
		libavcodec/dv_profile_internal.h \
		libavcodec/error_resilience.h \
		libavcodec/fdctdsp.h \
		libavcodec/flac.h \
		libavcodec/fft.h \
		libavcodec/fft-internal.h \
		libavcodec/fft_table.h \
		libavcodec/frame_thread_encoder.h \
		libavcodec/get_bits.h \
		libavcodec/h263dsp.h \
		libavcodec/h264chroma.h \
		libavcodec/h264pred.h \
		libavcodec/hpeldsp.h \
		libavcodec/idctdsp.h \
		libavcodec/internal.h \
		libavcodec/mathops.h \
		libavcodec/me_cmp.h \
		libavcodec/motion_est.h \
		libavcodec/mpegpicture.h \
		libavcodec/mpegutils.h \
		libavcodec/mpegvideo.h \
		libavcodec/mpegvideodsp.h \
		libavcodec/mpegvideoencdsp.h \
		libavcodec/old_codec_ids.h \
		libavcodec/options_table.h \
		libavcodec/pcm_tablegen.h \
		libavcodec/pel_template.c \
		libavcodec/pixblockdsp.h \
		libavcodec/pixels.h \
		libavcodec/pthread_internal.h \
		libavcodec/put_bits.h \
		libavcodec/qpeldsp.h \
		libavcodec/ratecontrol.h \
		libavcodec/rectangle.h \
		libavcodec/rl.h \
		libavcodec/rnd_avg.h \
		libavcodec/thread.h \
		libavcodec/tpel_template.c \
		libavcodec/version.h \
		libavcodec/videodsp.h \
		libavcodec/vorbis_parser_internal.h \
		libavcodec/vp3data.h \
		libavcodec/vp3dsp.h \
		libavcodec/vp56.h \
		libavcodec/vp56dsp.h \
		libavcodec/vp8data.h \
		libavcodec/vp8.h \
		libavcodec/vp8dsp.h \
		libavformat/audiointerleave.h \
		libavformat/avio_internal.h \
		libavformat/avformat.h \
		libavformat/dv.h \
		libavformat/internal.h \
		libavformat/pcm.h \
		libavformat/rdt.h \
		libavformat/rtp.h \
		libavformat/rtpdec.h \
		libavformat/spdif.h \
		libavformat/srtp.h \
		libavformat/options_table.h \
		libavformat/version.h \
		libavformat/w64.h \
		libswresample/swresample.h \
		libswresample/version.h \
		compat/va_copy.h "

manual_files="	libavutil/x86/x86inc.asm \
		libavutil/x86/x86util.asm \
		libavcodec/x86/hpeldsp_rnd_template.c \
		libavcodec/x86/rnd_template.c \
                libavcodec/x86/autorename_libavcodec_x86_videodsp_init.c \
		libavcodec/x86/autorename_libavcodec_x86_vorbisdsp_init.c \
		libavcodec/x86/constants.c \
		libavcodec/x86/fft_init.c \
		libavcodec/x86/h264_intrapred_init.c \
		libavcodec/x86/hpeldsp_init.c \
		libavcodec/x86/vp3dsp_init.c \
		libavcodec/x86/vp8dsp_init.c \
		libavutil/x86/autorename_libavutil_x86_cpu.c \
		libavutil/x86/autorename_libavutil_x86_float_dsp_init.c \
		libavutil/x86/lls_init.c \
		libavcodec/x86/deinterlace.asm \
		libavcodec/x86/fft.asm \
		libavcodec/x86/fpel.asm \
		libavcodec/x86/h264_intrapred.asm \
		libavcodec/x86/h264_intrapred_10bit.asm \
		libavcodec/x86/hpeldsp.asm \
		libavcodec/x86/videodsp.asm \
		libavcodec/x86/vorbisdsp.asm \
		libavcodec/x86/vp3dsp.asm \
		libavcodec/x86/vp8dsp.asm \
		libavcodec/x86/vp8dsp_loopfilter.asm \
		libavutil/x86/cpuid.asm \
		libavutil/x86/float_dsp.asm \
		libavutil/x86/lls.asm \
		libavcodec/bit_depth_template.c \
		libavcodec/fft_template.c \
		libavcodec/h264pred_template.c \
		libavcodec/hpel_template.c \
		libavcodec/hpeldsp_template.c \
		libavcodec/mdct_template.c \
		libavcodec/videodsp_template.c \
		libavcodec/h264pred.c \
		libavcodec/hpeldsp.c \
		libavcodec/videodsp.c \
		libavcodec/vp3.c \
		libavcodec/vp3_parser.c \
		libavcodec/vp3dsp.c \
		libavcodec/vp56rac.c \
		libavcodec/vp8.c \
		libavcodec/vp8_parser.c \
		libavcodec/vp8dsp.c \
		chromium/ffmpeg_stub_headers.fragment \
		chromium/ffmpegsumo.sigs"

other_files="	Changelog \
		COPYING.GPLv2 \
		COPYING.GPLv3 \
		COPYING.LGPLv2.1 \
		COPYING.LGPLv3 \
		CREDITS \
		ffmpeg_generated.gypi \
		ffmpeg.gyp \
                ffmpegsumo.ver \
		INSTALL \
		LICENSE \
		MAINTAINERS \
		OWNERS \
		README \
		README.chromium \
		RELEASE \
		xcode_hack.c "

files=$generated_files$manual_files$other_files$generated_files_headers$header_files

prefix="tmp_"

for f in $files
do
	dir_name=`echo $f | sed 's%/[^/]*$%/%'`
	if [[ $dir_name == */* ]]; then
		tmp_dir_name=$prefix$dir_name
		mkdir -p ../tmp_ffmpeg/$tmp_dir_name
	else
		tmp_dir_name=$f
	fi

	cp $f ../tmp_ffmpeg/$tmp_dir_name 2>/dev/null
done

mkdir -p ../tmp_ffmpeg/tmp_chromium/config
cp -r chromium/config ../tmp_ffmpeg/tmp_chromium

cd ../tmp_ffmpeg
for tmp_directory in $(find . -type d -name 'tmp_*')
do
	new_name=`echo $tmp_directory | sed 's/tmp_//'`
	mv $tmp_directory $new_name
done

cd ..
rm -rf ffmpeg
mv tmp_ffmpeg ffmpeg

cd $where
