%define festivalversion 1.96
# we ship the 1.4.2 docs for now.
%define docversion 1.4.2
%define speechtoolsversion 1.2.96

Name: festival
Summary: Speech synthesis and text-to-speech system
Version: %{festivalversion}
Release: 24%{?dist}

URL: http://www.cstr.ed.ac.uk/projects/festival/
Group: Applications/Multimedia
# the emacs file is GPL+, there is one TCL licensed source file
License: MIT and GPL+ and TCL


# Files needed for everything...
%define baseURL  http://festvox.org/packed/festival/%{festivalversion}
Source0: %{baseURL}/festival-%{festivalversion}-beta.tar.gz
Source1: %{baseURL}/speech_tools-%{speechtoolsversion}-beta.tar.gz

# Docs haven't been updated yet; here's the old ones
Source2: http://festvox.org/packed/festival/%{docversion}/festdoc-%{docversion}.tar.gz

# Our local site config files.
Source50: festival-1.96-0.7-fedora-siteinit.scm
Source51: festival-1.96-0.7-fedora-sitevars.scm

### DICTIONARIES
# Generic English dictionary
Source100: %{baseURL}/festlex_POSLEX.tar.gz
# American English dictionary
Source101: %{baseURL}/festlex_CMU.tar.gz
# OALD isn't included because it's got a more restrictive (non-commercial
# only) license. OALD voices not included for same reason.

# Note on voice versions: I'm simply using the file date of the newest file
# in each set of tarballs. It happens that the dates for all files from each
# source (diphone, cmu_arctic, etc.) match, which is handy.

### DIPHONE VOICES
%define diphoneversion 0.19990610
Source200: %{baseURL}/festvox_kallpc16k.tar.gz
Source202: %{baseURL}/festvox_kedlpc16k.tar.gz

### HTS VOICES (use Nagoya Institute of Technology's HTS based synthesizer)
# The Festvox site packages older versions of these as cmu_us_*_hts.
# These are from <http://hts.sp.nitech.ac.jp/>.
# And, ugh, the files seem to be only served via a script, not directly.
%define nitechbaseURL http://hts.sp.nitech.ac.jp/?plugin=attach&refer=Download&openfile=
%define nitechhtsversion 0.20061229
Source220: %{nitechbaseURL}/festvox_nitech_us_awb_arctic_hts.tar.bz2
Source221: %{nitechbaseURL}/festvox_nitech_us_bdl_arctic_hts.tar.bz2
Source222: %{nitechbaseURL}/festvox_nitech_us_clb_arctic_hts.tar.bz2
Source223: %{nitechbaseURL}/festvox_nitech_us_jmk_arctic_hts.tar.bz2
Source224: %{nitechbaseURL}/festvox_nitech_us_rms_arctic_hts.tar.bz2
Source225: %{nitechbaseURL}/festvox_nitech_us_slt_arctic_hts.tar.bz2

### Hispavoces Spanish voices http://forja.guadalinex.org/repositorio/projects/hispavoces/
%define hispavocesversion 1.0.0
Source300: http://v4.guadalinex.org/guadalinex-toro/pool-test/main/f/festival-spanish-voices/festival-spanish-voices_1.0.0.orig.tar.gz
Source301: COPYING.hispavoces

### Multisyn voices left out because they're ~ 100MB each.

### MBROLA voices left out, because they require MBROLA, which ain't free.


# Set defaults to American English instead of British English - the OALD
# dictionary (free for non-commercial use only) is needed for BE support
# Additionally, prefer the smaller (and I think nicer sounding) nitech hts
# voices.
Patch1: festival-1.96-nitech-american.patch

# Whack some buildroot references
Patch2: festival_buildroot.patch

# Use shared libraries
Patch3: festival-1.96-speechtools-shared-build.patch

# Fix a coding error (see bug #162137). Need to upstream.
Patch5: festival-1.96-speechtools-rateconvtrivialbug.patch

# Link libs with libm, libtermcap (see bug #198190).
# Need to upstream this.
Patch6: festival-1.96-speechtools-linklibswithotherlibs.patch

# For some reason, CXX is set to gcc on everything but Mac OS Darwin,
# where it's set to g++. Yeah, well. We need it to be right too.
Patch7: festival-1.96-speechtools-ohjeezcxxisnotgcc.patch

# Look for siteinit and sitevars in /etc/festival
Patch8: festival-1.96-etcsiteinit.patch

# Alias old cmu names to new nitech ones
Patch9: festival-1.96-alias_cmu_to_nitech.patch

# Look for speech tools here, not back there.
Patch10: festival-1.96-findspeechtools.patch

# Build main library as shared, not just speech-tools
Patch11: festival-1.96-main-shared-build.patch

# This is a hack to make the shared libraries build with actual
# sonames. Should pretty much do the right thing, although note
# of course that the sonames aren't official upstream.
Patch12: festival-1.96-bettersonamehack.patch

# this updates speech_tools to a development version which fixes
# a 64-bit cleanliness issue (among other changes).
Patch20: festival-1.96-speechtools-1.2.96-beta+awb.patch

# This makes festival use /usr/lib[arch]/festival/etc for its
# arch-specific "etc-path", rather than /usr/share/festival/etc/system_type.
# Then I use sed to replace the token with actual arch-specific libdir.
# A better way would be to actually make this a flexible makefile parameter,
# but that's something to take up with upstream.
Patch31: festival-1.96-kludge-etcpath-into-libarch.patch

# For some reason, the Nitech voices (and the previous CMU versions) fail to
# define proclaim_voice, which makes them not show up in the voice
# descriptions, which makes gnome-speech not show them.
Patch90: festival-1.96-nitech-proclaimvoice.patch

# Cure "SIOD ERROR: unbound variable : f2b_f0_lr_start"
Patch91: festival-1.96-nitech-fixmissingrequire.patch

# An apparent copy-paste error in these voices -- slt is referenced
# in all of them.
Patch92: festival-1.96-nitech-sltreferences.patch

Patch93: gcc43.patch

# Native pulseaudio support, https://bugzilla.redhat.com/show_bug.cgi?id=471047
Patch94: festival-speech-tools-pulse.patch

Patch95: gcc44.patch

# gcc 4.7 is finnicky about ambiguous function references'
Patch96: festival.gcc47.patch

# Bring back old patch since gcc 4.7 no longer ignores unknown options
Patch97: no-shared-data.patch

BuildRequires: pulseaudio-libs-devel
BuildRequires: tetex
BuildRequires: ncurses-devel

# Requires: festival-voice
# The hard dep below provides a festival-voice, no need to require it here.

# This is hard-coded as a requirement because it's the smallest voice (and,
# subjectively I think the most pleasant to listen to and so a good
# default).
#
# Ideally, this would be a "suggests" instead of a hard requirement.
#
# Update: with the new nitech versions of the voices, slt-arctic is no
# longer the smallest. But... AWB has a strong scottish accent, and JMK a
# kind of odd canadian one, so they're not great candidates for inclusion.
# And I find RMS a bit hard to understand. BDL isn't much smaller than SLT,
# and since I like it better, I think I'm going to keep it as the default
# for a price 12k. So, in case anyone later questions why this is the
# default, there's the answer. :)
Requires: festvox-slt-arctic-hts

Requires: festival-lib = %{version}-%{release}
Requires: festival-speechtools-libs = %{speechtoolsversion}-%{release}

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{festivalversion}-%{release}-XXXXXX)



%package lib
Summary: Library for the Festival speech synthesis system
# this is here to make sure upgrades go cleanly. In other cases,
# the auto-deps should handle this just fine.
Requires: festival-speechtools-libs = %{speechtoolsversion}-%{release}
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%package docs
Summary: Documentation for the Festival speech synthesis system
Group: Applications/Multimedia
Version: %{docversion}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
BuildArch: noarch

%package speechtools-libs
Summary: The Edinburgh Speech Tools libraries
Group: System Environment/Libraries
Version: %{speechtoolsversion}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%package speechtools-utils
Summary: Miscellaneous utilities from the Edinburgh Speech Tools
Group: Applications/Multimedia
Version: %{speechtoolsversion}

%package speechtools-devel
Summary: Development files for Edinburgh Speech Tools libraries
Version: %{speechtoolsversion}
Group: Development/Libraries
# Note: rpmlint complains incorrectly about
# "no-dependency-on festival-speechtools".
Requires: festival-speechtools-libs = %{speechtoolsversion}-%{release}

%package -n festvox-kal-diphone
Group: Applications/Multimedia
Summary: American English male speaker "Kevin" for Festival
Version: %{diphoneversion}
Provides: festival-voice
Provides: festvox-kallpc16k
BuildArch: noarch

%package -n festvox-ked-diphone
Group: Applications/Multimedia
Summary: American English male speaker "Kurt" for Festival
Version: %{diphoneversion}
Requires: festival
Provides: festival-voice
Provides: festvox-kedlpc16k
BuildArch: noarch

%package -n festvox-awb-arctic-hts
Group: Applications/Multimedia
Summary: Scottish-accent US English male speaker "AWB" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-bdl-arctic-hts
Group: Applications/Multimedia
Summary: US English male speaker "BDL" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-clb-arctic-hts
Group: Applications/Multimedia
Summary: US English female speaker "CLB" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-jmk-arctic-hts
Group: Applications/Multimedia
Summary: Canadian-accent US English male speaker "JMK" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-rms-arctic-hts
Group: Applications/Multimedia
Summary: US English male speaker "RMS" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-slt-arctic-hts
Group: Applications/Multimedia
Summary: US English female speaker "SLT" for Festival
Version: %{nitechhtsversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n hispavoces-pal-diphone
Group: Applications/Multimedia
Summary: Male Spanish voice «PAL» for Festival
Version: %{hispavocesversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n hispavoces-sfl-diphone
Group: Applications/Multimedia
Summary: Female Spanish voice «SFL» for Festival
Version: %{hispavocesversion}
Requires: festival
Provides: festival-voice
BuildArch: noarch

# This is last as a lovely hack to make sure Version gets set back
# to what it should be. Grr.
%package devel
Summary: Development files for the Festival speech synthesis system
Version: %{festivalversion}
Group: Development/Libraries
# Note: rpmlint complains incorrectly about
# "no-dependency-on festival"
Requires: festival-speechtools-devel = %{speechtoolsversion}-%{release}
Requires: festival-lib = %{version}-%{release}
Requires: festival-lib



%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

%description lib
The shared library used by the Festival text-to-speech and speech synthesis
system.

%description docs
HTML, Postscript, and Texinfo documentation for the Festival text-to-speech
and speech synthesis system.

%description speechtools-libs
The Edinburgh Speech Tools libraries, used by the Festival text-to-speech
and speech synthesis system.

%description speechtools-utils 
Miscellaneous utilities from the Edinburgh Speech Tools. Unless you have a
specific need for one of these programs, you probably don't need to install
this.

%description speechtools-devel
Development files for the Edinburgh Speech Tools Library, used by the
Festival speech synthesis system.


%description -n festvox-kal-diphone
American English male speaker ("Kevin") for Festival.

This voice provides an American English male voice using a residual excited
LPC diphone synthesis method. It uses the CMU Lexicon pronunciations.
Prosodic phrasing is provided by a statistically trained model using part of
speech and local distribution of breaks. Intonation is provided by a CART
tree predicting ToBI accents and an F0 contour generated from a model
trained from natural speech. The duration model is also trained from data
using a CART tree.


%description -n festvox-ked-diphone
American English male speaker ("Kurt") for Festival.

This voice provides an American English male voice using a residual excited
LPC diphone synthesis method. It uses the CMU Lexicon for pronunciations.
Prosodic phrasing is provided by a statistically trained model using part of
speech and local distribution of breaks. Intonation is provided by a CART
tree predicting ToBI accents and an F0 contour generated from a model
trained from natural speech. The duration model is also trained from data
using a CART tree.


%description -n festvox-awb-arctic-hts
US English male speaker ("AWB") for Festival. AWB is a native Scottish
English speaker, but the voice uses the US English front end.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1138 utterances spoken by a Scottish English male speaker. The
speaker is very experienced in building synthetic voices and matched
prompted US English, though his vowels are very different from US English
vowels. Scottish English speakers will probably find synthesizers based on
this voice strange. Unlike the other CMU_ARCTIC databases this was recorded
in 16 bit 16KHz mono without EGG, on a Dell Laptop in a quiet office. The
database was automatically labelled using CMU Sphinx using the FestVox
labelling scripts. No hand correction has been made.


%description -n festvox-bdl-arctic-hts
US English male speaker ("BDL") for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using CMU Sphinx using
the FestVox labelling scripts. No hand correction has been made.


%description -n festvox-clb-arctic-hts
US English female speaker ("CLB") for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English female speaker. The
speaker is experienced in building synthetic voices. This was recorded at
16bit 32KHz, in a sound proof room, in stereo, one channel was the waveform,
the other EGG. The database was automatically labelled using CMU Sphinx
using the FestVox labelling scripts. No hand correction has been made.


%description -n festvox-jmk-arctic-hts
US English male speaker ("JMK") voice for Festival. JMK is a native Canadian
English speaker, but the voice uses the US English front end.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1138 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using CMU Sphinx using
the FestVox labelling scripts. No hand correction has been made.

%description -n festvox-rms-arctic-hts
US English male speaker ("RMS") voice for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using EHMM an HMM labeler
that is included in the FestVox distribution. No hand correction has been
made.

%description -n festvox-slt-arctic-hts
US English female speaker ("SLT") voice for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English female speaker. The
speaker is experienced in building synthetic voices. This was recorded at
16bit 32KHz, in a sound proof room, in stereo, one channel was the waveform,
the other EGG. The database was automatically labelled using CMU Sphinx
using the FestVox labelling scripts. No hand correction has been made.

%description -n hispavoces-sfl-diphone
Female Castillian-Spanish (es_ES) voice «SFL» for Festival.

This is a diphone-based male Spanish voice for the Festival speech synthesis
system. These original audio files were recorded by a professional voice
talent in a recording studio.

This voice was developed by the Consejeria de Innovacion, Ciencia y Empresa
of the Junta de Andalucia on a project awarded to MP Sistemas in
collaboration with Intelligent Dialogue Systems (INDISYS).

The primary objective was to integrate a higher-quality diphone-based
Spanish voice in Guadalinex v4.0, an Ubuntu-based Linux distribution
promoted by the Government of Andalusia (Spain). See
http://www.guadalinex.org for more information.

%description -n hispavoces-pal-diphone
Male Castillian-Spanish (es_ES) voice «PAL» for Festival.

This is a diphone-based male Spanish voice for the Festival speech synthesis
system. These original audio files were recorded by a professional voice
talent in a recording studio.

This voice was developed by the Consejeria de Innovacion, Ciencia y Empresa
of the Junta de Andalucia on a project awarded to MP Sistemas in
collaboration with Intelligent Dialogue Systems (INDISYS).

The primary objective was to integrate a higher-quality diphone-based
Spanish voice in Guadalinex v4.0, an Ubuntu-based Linux distribution
promoted by the Government of Andalusia (Spain). See
http://www.guadalinex.org for more information.

%description devel
Development files for the Festival speech synthesis system. Install
festival-devel if you want to use Festival's capabilities from within your
own programs, or if you intend to compile other programs using it. Note that
you can also interface with Festival in via the shell or with BSD sockets.



%prep
%setup -q -n festival -a 1

# speech tools
%setup -q -n festival -D -T -a 2

# exit out if they've fixed this, so we can remove this hack.
[ -x speech_tools/base_class/string/EST_strcasecmp.c ] || exit 1
chmod -x speech_tools/base_class/string/EST_strcasecmp.c

# dictionaries
%setup -q -n festival -D -T -b 100
%setup -q -n festival -D -T -b 101

# voices
%setup -q -n festival -D -T -b 200
%setup -q -n festival -D -T -b 202
%setup -q -n festival -D -T -b 220
%setup -q -n festival -D -T -b 221
%setup -q -n festival -D -T -b 222
%setup -q -n festival -D -T -b 223
%setup -q -n festival -D -T -b 224
%setup -q -n festival -D -T -b 225
%setup -c -q -n festival -D -T -b 300

%patch1 -p1 -b .nitech
%patch2 -p1 -b .buildrootrefs
%patch3 -p1 -b .shared
%patch5 -p1 -b .bugfix
%patch6 -p1 -b .liblinking
%patch7 -p1 -b .cxx
%patch8 -p1 -b .etc
%patch9 -p1 -b .cmu2nitech
# patch9 creates a new file; patch helpfully makes a "backup" of the
# non-existent "original", which then has bad permissions. zap.
rm -f lib/alias_cmu_to_nitech.scm.cmu2nitech
%patch10 -p1 -b .findspeechtools
%patch11 -p1 -b .shared
%patch12 -p1 -b .soname

%patch20 -p1 -b .awb

%patch31 -p1 -b .libarch
# finish the kludge for arch-specific "etc" (misc. binaries)
for f in speech_tools/main/siod_main.cc src/arch/festival/festival.cc; do
  sed -i -e 's,{{HORRIBLELIBARCHKLUDGE}},"%{_libdir}",' $f
done

# no backups for these patches because
# the voice directories are copied wholesale
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1 -b .gcc43
%patch94 -p1 -b .pulse
%patch95 -p1 -b .gcc44
%patch96 -p0 -b .gcc47
%patch97 -p1 -b .no-share

# zero length
rm festdoc-%{docversion}/speech_tools/doc/index_html.jade
rm festdoc-%{docversion}/speech_tools/doc/examples_gen/error_example_section.sgml
rm festdoc-%{docversion}/speech_tools/doc/tex_stuff.jade



%build

# build speech tools (and libraries)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
pushd speech_tools
  %configure
  # -fPIC 'cause we're building shared libraries and it doesn't hurt
  # -fno-strict-aliasing because of a couple of warnings about code
  #   problems; if $RPM_OPT_FLAGS contains -O2 or above, this puts
  #   it back. Once that problem is gone upstream, remove this for
  #   better optimization.
  make \
    CFLAGS="$RPM_OPT_FLAGS -fPIC -fno-strict-aliasing" \
    CXXFLAGS="$RPM_OPT_FLAGS  -fPIC -fno-strict-aliasing"
popd

# build the main program
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/lib
# instead of doing this, maybe we should patch the make process
# so it looks in the right place explicitly:
export PATH=$(pwd)/bin:$PATH
%configure
make \
  FTLIBDIR="%{_datadir}/festival/lib" \
  CFLAGS="$RPM_OPT_FLAGS -fPIC" \
  CXXFLAGS="$RPM_OPT_FLAGS -fPIC"

# build the patched CMU dictionary
pushd lib/dicts/cmu
  make
popd


%install
# "make install" for this package is, um, "interesting". It seems geared for
# local user-level builds. So, rather than doing that and then patching it
# up, do the right parts by hand as necessary.

# install speech tools libs, binaries, and include files
pushd speech_tools

  make INSTALLED_LIB=$RPM_BUILD_ROOT%{_libdir} make_installed_lib_shared
  # no thanks, static libs.
  rm $RPM_BUILD_ROOT%{_libdir}/*.a

  make INSTALLED_BIN=$RPM_BUILD_ROOT%{_libexecdir}/speech-tools make_installed_bin_static
  # this list of the useful programs in speech_tools comes from
  # upstream developer Alan W. Black; the other stuff is to be removed.
  pushd $RPM_BUILD_ROOT%{_libexecdir}/speech-tools
    ls |
        grep -Evw "ch_wave|ch_track|na_play|na_record|wagon|wagon_test" |
        grep -Evw "make_wagon_desc|pitchmark|pm|sig2fv|wfst_build" |
        grep -Evw "wfst_run|wfst_run" |
        xargs rm
  popd

  pushd include
    for d in $( find . -type d | grep -v win32 ); do
      make -w -C $d INCDIR=$RPM_BUILD_ROOT%{_includedir}/speech_tools/$d install_incs
    done
    # Um, yeah, so, "EST" is not a very meaningful name for the include dir.
    # The Red Hat / Fedora package has traditionally put this stuff under
    # "speech_tools", and that's what we're gonna do here too.
    mv $RPM_BUILD_ROOT%{_includedir}/speech_tools/EST/*.h \
       $RPM_BUILD_ROOT%{_includedir}/speech_tools/
    rmdir $RPM_BUILD_ROOT%{_includedir}/speech_tools/EST
    mv $RPM_BUILD_ROOT%{_includedir}/speech_tools/unix/EST/EST_* \
       $RPM_BUILD_ROOT%{_includedir}/speech_tools/unix/
    rmdir $RPM_BUILD_ROOT%{_includedir}/speech_tools/unix/EST
    mv $RPM_BUILD_ROOT%{_includedir}/speech_tools/instantiate/EST/instantiate/EST_* \
       $RPM_BUILD_ROOT%{_includedir}/speech_tools/instantiate/
    rm -rf $RPM_BUILD_ROOT%{_includedir}/speech_tools/instantiate/EST
    mv $RPM_BUILD_ROOT%{_includedir}/speech_tools/sigpr/EST/EST_* \
       $RPM_BUILD_ROOT%{_includedir}/speech_tools/sigpr
    rmdir $RPM_BUILD_ROOT%{_includedir}/speech_tools/sigpr/EST
    mv $RPM_BUILD_ROOT%{_includedir}/speech_tools/ling_class/EST/EST_* \
       $RPM_BUILD_ROOT%{_includedir}/speech_tools/ling_class
    rmdir $RPM_BUILD_ROOT%{_includedir}/speech_tools/ling_class/EST
  popd

  cp README ../README.speechtools

popd

# install the dictionaries
TOPDIR=$( pwd )
pushd lib/dicts
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/dicts
  # we want to put the licenses in the docs...
  cp COPYING.poslex $OLDPWD/COPYING.poslex
  cp cmu/COPYING $OLDPWD/COPYING.cmudict
  for f in wsj.wp39.poslexR wsj.wp39.tri.ngrambin ; do
    install -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/lib/dicts/
  done
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/dicts/cmu
  pushd cmu
    # note I'm keeping cmudict-0.4.diff and cmudict_extensions.scm to
    # satisfy the "all changes clearly marked" part of the license -- these
    # are the changes. And yes, the ".out" file is the one actually used.
    # Sigh.
    for f in allowables.scm cmudict-0.4.diff cmudict-0.4.out \
             cmudict_extensions.scm cmulex.scm cmu_lts_rules.scm; do
      install -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/lib/dicts/cmu/
    done
  popd
popd

# install the voices
pushd lib/voices
  # get the licenses. This is probably too clever by half, but oh well.
  for f in $( find . -name COPYING ); do
    n=$( echo $f | sed 's/.*\/\(.*\)\/COPYING/COPYING.\1/' )
    mv $f $OLDPWD/$n
  done
  # ditch the readme files -- these aren't very useful.
  # Except keep a README.htsvoice, because it contains license information.
  cp us/nitech_us_awb_arctic_hts/hts/README.htsvoice $OLDPWD/README.htsvoice
  find . -name 'README*' -exec rm {} \;
popd
# kludge! nitech_us_awb_arctic_hts is missing its COPYING file. It should
# be the same as the other nitech files, though, so just copy one.
cp COPYING.nitech_us_bdl_arctic_hts COPYING.nitech_us_awb_arctic_hts
cp -a lib/voices $RPM_BUILD_ROOT%{_datadir}/festival/lib

mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/voices/es/
cp -a festival-spanish-voices-1.0.0/* $RPM_BUILD_ROOT%{_datadir}/festival/lib/voices/es/
cp %{SOURCE301} .

# okay, now install the main festival program.

# binaries:
make INSTALLED_BIN=$RPM_BUILD_ROOT%{_bindir} make_installed_bin_static
install -m 755 bin/text2wave $RPM_BUILD_ROOT%{_bindir}

# install the shared library
cp -a src/lib/libFestival.so* $RPM_BUILD_ROOT%{_libdir}

# this is just nifty. and it's small.
install -m 755 examples/saytime $RPM_BUILD_ROOT%{_bindir}

# man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -a doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# lib: the bulk of the program -- the scheme stuff and so on
pushd lib
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib
  for f in *.scm festival.el *.ent *.gram *.dtd *.ngrambin speech.properties ; do
    install -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/lib/
  done
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/multisyn/
  install -m 644 multisyn/*.scm $RPM_BUILD_ROOT%{_datadir}/festival/lib/multisyn/
popd

# "etc" -- not in the configuration sense, but in the sense of "extra helper
# binaries".
pushd lib/etc
  # not arch-specific
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/lib/etc
  install -m 755 email_filter $RPM_BUILD_ROOT%{_datadir}/festival/lib/etc
  # arch-specific
  mkdir -p $RPM_BUILD_ROOT%{_libdir}/festival/etc
  install -m 755 */audsp $RPM_BUILD_ROOT%{_libdir}/festival/etc
popd

# the actual /etc. :)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/festival
# use our version of this file
rm $RPM_BUILD_ROOT%{_datadir}/festival/lib/siteinit.scm
install -m 644 %{SOURCE50} $RPM_BUILD_ROOT%{_sysconfdir}/festival/siteinit.scm
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/festival/sitevars.scm

# copy in the intro.text. It's small and makes (intro) work. in the future,
# we may want include more examples in an examples subpackage
mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/examples/
install -m 644 examples/intro.text $RPM_BUILD_ROOT%{_datadir}/festival/examples


# header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/festival
cp -a src/include/* $RPM_BUILD_ROOT%{_includedir}/festival

# Clean up some junk from the docs tarball.
pushd festdoc-%{docversion}/speech_tools/doc
  rm -fr CVS arch_doc/CVS man/CVS  speechtools/arch_doc/CVS
  rm -f .*_made .speechtools_html .tex_done
popd

# info pages
mkdir -p $RPM_BUILD_ROOT%{_infodir}
cp -p festdoc-%{docversion}/festival/info/* $RPM_BUILD_ROOT%{_infodir}



%clean
rm -rf $RPM_BUILD_ROOT



%post docs
/sbin/install-info %{_infodir}/festival.info.gz %{_infodir}/dir --section "Accessibility" > /dev/null 2>&1
:

%post lib -p /sbin/ldconfig

%post speechtools-libs -p /sbin/ldconfig


%postun docs
if [ "$1" = 0 ]; then
        /sbin/install-info --delete %{_infodir}/festival.info.gz %{_infodir}/dir --section "Accessibility" > /dev/null 2>&1
fi
:

%postun lib -p /sbin/ldconfig

%postun speechtools-libs -p /sbin/ldconfig



%files
%defattr(-,root,root)
%doc ACKNOWLEDGMENTS COPYING NEWS README
%doc COPYING.poslex COPYING.cmudict
%dir %{_sysconfdir}/festival
%config(noreplace)  %{_sysconfdir}/festival/siteinit.scm
%config(noreplace)  %{_sysconfdir}/festival/sitevars.scm
%{_bindir}/festival
%{_bindir}/festival_client
%{_bindir}/festival_server
%{_bindir}/festival_server_control
%{_bindir}/text2wave
%{_bindir}/saytime
%dir %{_datadir}/festival
%dir %{_datadir}/festival/lib
%{_datadir}/festival/lib/*.scm
%{_datadir}/festival/lib/festival.el
%{_datadir}/festival/lib/*.ent
%{_datadir}/festival/lib/*.gram
%{_datadir}/festival/lib/*.dtd
%{_datadir}/festival/lib/*.ngrambin
%{_datadir}/festival/lib/speech.properties
%{_datadir}/festival/lib/dicts
%{_datadir}/festival/lib/etc
%dir %{_datadir}/festival/lib/multisyn
%{_datadir}/festival/lib/multisyn/*.scm
%dir %{_datadir}/festival/examples
%{_datadir}/festival/examples/intro.text
%dir %{_libdir}/festival
%dir %{_libdir}/festival/etc
%{_libdir}/festival/etc/*
%{_mandir}/man1/*

%files lib
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libFestival.so.*

%files docs
%defattr(-,root,root)
%doc festdoc-%{docversion}/festival/html/*html
%{_infodir}/*

%files speechtools-libs
%defattr(-,root,root)
%doc README.speechtools
%{_libdir}/libestbase.so.*
%{_libdir}/libestools.so.*
%{_libdir}/libeststring.so.*

%files speechtools-utils
%defattr(-,root,root)
%doc README.speechtools
%dir %{_libexecdir}/speech-tools
%{_libexecdir}/speech-tools/*

%files speechtools-devel
%defattr(-,root,root)
%doc festdoc-%{docversion}/speech_tools
%{_libdir}/libestbase.so
%{_libdir}/libestools.so
%{_libdir}/libeststring.so
%dir %{_includedir}/speech_tools
%{_includedir}/speech_tools/*

%files -n festvox-kal-diphone
%defattr(-,root,root)
%doc COPYING.kal_diphone
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/english
%{_datadir}/festival/lib/voices/english/kal_diphone

%files -n festvox-ked-diphone
%defattr(-,root,root)
%doc COPYING.ked_diphone
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/english
%{_datadir}/festival/lib/voices/english/ked_diphone

%files -n festvox-awb-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_awb_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_awb_arctic_hts

%files -n festvox-bdl-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_bdl_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_bdl_arctic_hts

%files -n festvox-clb-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_clb_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_clb_arctic_hts

%files -n festvox-jmk-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_jmk_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_jmk_arctic_hts

%files -n festvox-rms-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_rms_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_rms_arctic_hts

%files -n festvox-slt-arctic-hts
%defattr(-,root,root)
%doc COPYING.nitech_us_slt_arctic_hts COPYING.hts README.htsvoice
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/us
%{_datadir}/festival/lib/voices/us/nitech_us_slt_arctic_hts

%files -n hispavoces-pal-diphone
%defattr(-,root,root)
%doc COPYING.hispavoces
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/es
%dir %{_datadir}/festival/lib/voices/es/JuntaDeAndalucia_es_pa_diphone/
%{_datadir}/festival/lib/voices/es/JuntaDeAndalucia_es_pa_diphone/*

%files -n hispavoces-sfl-diphone
%defattr(-,root,root)
%doc COPYING.hispavoces
%dir %{_datadir}/festival/lib/voices
%dir %{_datadir}/festival/lib/voices/es
%dir %{_datadir}/festival/lib/voices/es/JuntaDeAndalucia_es_sf_diphone/
%{_datadir}/festival/lib/voices/es/JuntaDeAndalucia_es_sf_diphone/*

%files devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libFestival.so
%dir %{_includedir}/festival
%{_includedir}/festival/*


%changelog
* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> - 1.96-24
- Minor Merge review fixes, BZ 225748.

* Mon Jan  7 2013 Matthias Clasen <mclasen@redhat.com> - 1.96-23
- Add tighter inter-subpackage deps (recommended by rpmdiff)

* Mon Jan  7 2013 Matthias Clasen <mclasen@redhat.com> - 1.96-22
- Fix directory ownership for /usr/share/festival/lib/voices/es

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 25 2012 Bruno Wolff III <bruno@wolff.to> - 1.96-20
- Fix to build with gcc 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 22 2011 Tim Niemueller <tim@niemueller.de> - 1.96-18
- Fix install paths of speech_tools includes (rhbz #242607)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-16
- Add native pulseaudio support (#471047)

* Thu Sep 10 2009 Bernie Innocenti <bernie@codewiz.org> - 1.96-15
- Disable esd support (resolves: rhbz#492982)

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-14
- Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 18 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-12
- Add Spanish voices from the guadalinex project, in the
  hispavoces-pal-diphone and hispavoces-sfl-diphone subpackages
  (#496011)

* Tue Mar 24 2009 Jesse Keating <jkeating@redhat.com> - 1.96-11
- Drop the explicit dep on festival-voice, as it is redundant and
  causes problems with multiple providers

* Thu Feb 26 2009 Matthias Clasen  <mclasen@redhat.com> 1.96-10
- Fix build with gcc 4.4

* Tue Feb 24 2009 Matthias Clasen  <mclasen@redhat.com> 1.96-9
- Make -docs and all the festvox subpackages noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 1.96-7
- Tweak summaries

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> - 1.96-6
- interoperate with other apps by using pacat for audio output
  (bug 467531)

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.96-5
- fix license tag

* Fri Feb 22 2008 Matthias Clasen  <mclasen@redhat.com> - 1.96-4
- Fix the build with gcc 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.96-3
- Autorebuild for GCC 4.3

* Wed Nov  7 2007 Stepan Kasal <skasal@redhat.com>1.96-2
- fix a typo in a summary and in festival-1.96-nitech-proclaimvoice.patch
- Resolves: #239216

* Tue Mar 20 2007 Ray Strode <rstrode@redhat.com> 1.96-1
- rebuild

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> 1.96-0.11
- Forgot to add the .scm files

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> 1.96-0.10
- Update to Matthew Miller's much improved package (#232105)
- Move the buildroot patch around

* Sun Mar 18 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.9
- fix the library link patch to use -lncurses instead of -ltinfo --
  the later is all that's really needed, but the former works on older
  distros too.

* Fri Mar 16 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.8
- festival-devel depends on the libraries package, not base festival. this
  raises an multilib question: need to obsolete festival.i386 on x86_64.
  Right now, there's no mechanism for doing that. Fortunately, all the
  changes in packaging happen to make it so that the current version doesn't
  conflict with the old release, so one will get unused cruft but not
  breakage when upgrading.
- Bite teh proverbial bullet and make libFestival build shared.
- update speech-tools soname patch to work in the more general case needed
  by the festival main build
- make said shared-lib a subpackage to avoid multiarching the whole thing
- split festival-devel and speechutils-devel in anticipation of future
  plan of actually decoupling these packages.
- note that rpmlint complains about "missing" deps on the devel packages. it
  should be fixed to recognize requiring a -lib/libs package is sufficent or
  better.
- add saytime script. Because, really, what else is this package *for*?
- add the intro.text so (intro) works. 196 more bytes won't kill us. :)
- remove $PATH from LD_LIBRARY_PATH used in build. (What the heck?)
- add defattr to all subpackages. I don't think it's strictly necessary
  since putting it in the first package seems sufficient, but that's
  probably not behavior to count on.
- make descriptions and summaries use more consistant language

* Thu Mar 15 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.7
- Upstream baseurl now includes version. (Thanks Alan Black @ cmu)
- Update siteinit patch to also incorporate sitevars
- Add sitevars as a config file
- Ship our own siteinit and sitevars as sources
- In default sitevars, reference /usr/local/share/festival/lib as another
  place to look for voices (it's okay if that doesn't exist). Hopefully,
  this will encourage people who want to install non-RPM-packaged voices to
  keep from doing it in /usr/share.
- Fix wrong references to slt voice in other nitech voices
- Fix wrongly commented-out (require 'f2bf0lr) in awb, clb, and rms voices.
- Stop untarring source files and use the setup macro properly.
- Get rid of silly DATA.TMP directories for installing voices and 
  dictionaries.
- Stop making ../speechtools link. Currently solved by patching to look
  in the current directory; could also do this by moving everything up
  a directory.
- TODO: festival-buildroot.patch could stand to be updated. May not
  even be needed anymore.
- Drop the 8k versions of the diphone voices, since there's not really
  any point. If you want smaller, use one of the arctic_hts voices
  instead. And overall, this saves us about 4.5M.

* Wed Mar 14 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.6
- Fix copy-paste error in JMK description (thanks Matthias Clasen)
- Remove "nitech-us-" from the names of those voice packages to make the
  package names shorter. (This will also be more convenient if we switch to
  the cmu versions in the future.)
- made aliases so old cmu_us_*_arctic_hts voice names still work.
- Look for /etc/festival/siteinit.scm (and move siteinit.scm there!)
- Mark siteinit.scm as a config file
- Remove some non-useful stuff from speech-tools-utils.
- Move main dir from /usr/share/festival to /usr/share/festival/lib at
  request of upstream. Also, we can drop the FHS (well, "fsstnd" -- it's
  old) patch and just pass FTLIBDIR to make. Which, hey, we were already
  doing. Yay redundancy.
- clean up CFLAGS and CXXFLAGS. "-fpermissive" was hiding bad stuff.
- update speech tools with patch from AWB to fix 64-bit build issue 
  with EST_DProbDist
- there's still some compiler warnings which should be addressed upstream.
- The nitech hts voices don't properly proclaim_voice, making them not
  show up for gnome-speech and thus making orca crash. See details in the
  comments in bug #232105.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.5
- use festvox- instead of festival-voice for voice packages -- matches
  upstream tarballs, and is shorter. Also, use shorter form of
  the date-based version.
- get the README.htsvoice from the nitech voices -- it contains
  license info.
- build (but don't enable by default) ESD support in speech-tools (bug
  #198908)
- fix coding error noted in bug #162137 -- need to push this upstream.
- link speech tools libraries with -lm, -ltermcap, -lesd and with themselves
  (bug #198190, partially)
- holy sheesh. Use g++ for CXX, not gcc. Fixes bug #198190 completely.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.4
- subpackages! Split out speech-tools, docs, voices.
- long descriptions for the individual voices, carefully gathered from
  readmes and web sites.
- ooh. replace cmu_hts voices with the updated versions from upstream
  <http://hts.sp.nitech.ac.jp/>. Two new voices, and updated versions of
  the others. (The voices packaged at festvox.org are apparently based on
  older versions of these, which in turn are from the CMU upstream.)
- TODO: make aliases for the cmu voices.
- arguably, voices should be made in to their own src.rpms. They don't need
  anything from here to build. That's for a future version. (At that time,
  the gigantic multisyn voices could be added.) The CMU dict needs festival
  installed to build, but I don't think it needs the source, so dicts could
  be subpackages too. And the docs are also a good candidate for separation.
  speech-tools, though, is incestuously used in the festival build process
  and I think it makes sense to keep that bundled.
- TODO: check through the speechtools-utils for what should actually be 
  packaged; fix the include path for siod (and anything else that needs it).
- TODO: package festival.el so it just works with emacs.
- TODO: reinvent festival_server_control as a proper init script
- TODO: put the festival server in sbin, maybe?
- Another question: should we drop the 8k diphone voices? Any point?
- Changed "X11-like" to "MIT-style" (which is what X11 is) to make rpmlint
  happy.
- make %%{festivalversion} macro to deal with all of the changes to version
  in subpackages. Kludgy, but there's RPM for you.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.3
- oh! The "etc-path" is important after all. Map that into
  /usr/lib[arch]/festival via a kludge.
- make cmu_us_slt_arctic_hts the default voice, in preparation for
  splitting the voice packages. (thankfully, there's already a fallback
  mechanism -- cool!)

* Mon Mar 12 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.2
- clean up accidental backup file left in updated awb_arctic_hts 
  tarball
- remove /usr/share/festival/etc (see bug #228315)
- move unpackage voices to the prep section where it belongs
- other minor spec file readability changes
- "make install" for this package is, um, "interesting". It seems
  geared for local user-level builds. So, rather than doing that and
  then patching it up, do the right parts by hand as necessary. (The
  previous version of the spec file did a convoluted mix of both.)
- don't install static libs.
- took out the massive hack that munges EST_*.h to speech_tools/EST_*.h in
  the installed header files -- programs should instead use
  -I/usr/include/speech_tools, shouldn't they? Put this back if I'm wrong.
- TODO -- autogenerated speech_tools docs
- festvox_ellpc11k.tar.gz, the spanish voice, wasn't getting installed anyway
  due to a license question. Since it's also gone upstream, removing.

* Fri Mar 09 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.1
- Preliminary update to 1.96
- Update to new cmu_us_*_arctic files -- they're changed upstream,
  although they don't appear to be versioned. Awesome. The current
  versions are those found in the same directory with the 1.96 files.
- ditto festlex_CMU.tar.gz
- add macro for speechtoolsversion
- minor update to festival-1.96-american.patch.
- update shared build patch and rename to make more obvious that
  it applies to the speechtools portion of the package.
- gcc 4 build patches now upstream.
- localhost-connections patch now upstream.
- note that festvox_ellpc11k.tar.gz and festvox_kallpc8k.tar.gz are no longer 
  in the directory tree upstream; drop?

* Fri Jan 19 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.95-6
- link with ncurses
- add dist tag
- make scriptlets safer

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 22 2006 Ray Strode <rstrode@redhat.com> - 1.95-5
- get gnopernicus working again. Patch from 
  Fernando Herrera <fherrera@gmail.com> (bug 178312)
- add a lot of compiler flags and random cruft to get
  festival to build with gcc 4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Florian La Roche <laroche@redhat.com>
- another try to get it to compile again

* Tue Apr 28 2005  <johnp@redhat.com> - 1.95-3
- require info packages so the post does not fail
- remove /usr/bin/VCLocalRule from buildroot since it is
  an extranious file that does not need to be installed

* Wed Apr 27 2005 Miloslav Trmac <mitr@redhat.com> - 1.95-2
- Fix build with gcc 4 (#156132)
- Require /sbin/install-info for scriptlets (#155698)
- Don't ship %%{_bindir}/VCLocalRules (#75645)

* Fri Feb 25 2005  <jrb@redhat.com> - 1.95-1
- patch from Matthew Miller to update to 1.95.  Full changelog below

* Mon Feb  7 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm8
- put speech-tools binaries in /usr/libexec/speech-tools so as to not
  clutter /usr/bin. Another approach would be to make speech-tools a 
  separate package and to make these utilities a subpackage of that.
- macro-ize /usr/bin, /usr/lib, /usr/include

* Sun Feb  6 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm6
- worked on this some more
- made actually work -- put back rest of fsstnd patch which I had broken
- made kludge for lack of sonames in shared libraries -- I think I did the
  right thing
- put back american as the default -- british dicts are non-free.

* Wed Jan  5 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm1
- preliminary update to 1.95 beta
- add really nice CMU_ARCTIC HTS voices, which is the whole point of wanting
  to do this. (They have a free license.)
- switch to festvox.org north american upstream urls
- keep old doc files -- there's no new ones yet.
- add comment to specfile about reason for lack of OALD (British) voices --
  they've got a more restrictive license.
- change license to "X11-style", because that's how they describe it.
- remove exclusivearch. I dunno if this builds on other archs, but I
  also don't know why it wouldn't.
- fancier buildroot string, 'cause hey, why not.
- more "datadir" macros
- remove most of Patch0 (fsstnd) -- can be done by setting variables instead.
  there's some bits in speechtools still, though
- update Patch3 (shared-build)
- don't apply patches 20 and 21 -- no longer needed.
- disable adding "FreeBSD" and "OpenBSD" to the dictionary for now. Probably
  a whole list of geek words should be added. Also, the patch was applied
  in an icky kludgy way.

* Thu Jul 29 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-25
- Update for gcc 3.4

* Wed Jul 28 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-24
- Use shared libraries to reduce package size
- Don't ship patch backup files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  4 2004 Jonathan Blandford <jrb@redhat.com> 1.4.2-21
- Remove the spanish voices until we get clarification on the license

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com>
- BR libtermcap-devel #104722

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 25 2003 Bill Nottingham <notting@redhat.com> 1.4.2-19
- clean up buildroot references (#75643, #77908, #102985)
- remove some extraneous scripts
- fix build with gcc-3.3

* Thu Jun 12 2003 Elliot Lee <sopwith@redhat.com> 1.4.2-17
- Rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Tim Powers <timp@redhat.com> 1.4.2-15
- redirect install-info spewage

* Tue Jan  7 2003 Jens Petersen <petersen@redhat.com> 1.4.2-14
- put info files in infodir
- add post and postun script to install and uninstall info dir file entry
- drop postscript and info files from docs

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.4.2-13
- rebuild

* Thu Aug 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.4.2-12
- Adapt to current libstdc++

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 1.4.2-10
- build using gcc-3.2-0.1

* Wed Jul  3 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-9
- Add some missing helpprograms (# 67698)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-7
- Fix some rpmlint errors

* Mon Jun 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.4.2-6
- Fix ISO C++ compliance

* Mon Mar 18 2002 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Mar 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-2
- Get rid of CVS directiories in doc dir
- Fix broken symlinks for components from speech_tools

* Wed Mar  6 2002 Trond Eivind Glomsrød <teg@redhat.com>
- 1.4.2
- Lots of fixes to make it build, more needed
- Cleanups
- Update URL
- Fix docs inclusion
- Drop prefix
- Use %%{_tmppath}

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add defattr (Bug #15033)

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix build on current 7.0

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix build on current 7.0

* Thu Jul  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build on non-x86

* Sun Apr 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial packaging
