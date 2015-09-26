# set to include Japanese and Korean tables
%define jk_tables 0

# set to include Indic tables
%define indic_tables 0

Name:           scim-tables
Version:        0.5.12
Release:        6%{?dist}
Summary:        SCIM Generic Table IMEngine

License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://sourceforge.net/projects/scim
Source0:        http://downloads.sourceforge.net/scim/%{name}-%{version}.tar.gz
Source1:        ZhuYin.txt.in
Source2:        ZhuYin-Big.txt.in
Source3:        Cantonese.txt.in
Source4:        CangJie5.txt.in
Source5:        CangJie5.png
BuildRoot:      %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

BuildRequires:  scim-devel, gtk2-devel
# if autotools scripts modified
BuildRequires:  gettext-devel automake libtool intltool
Requires:       scim
Patch1:         scim-tables-0.5.7-2.bz217639.patch
Patch2:	        scim-tables-0.5.7-5.bz232860.patch

%description
This package contains the Generic Table IMEngine for SCIM.

%package amharic
Summary:        SCIM tables for Amharic
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description amharic
This package contains scim-tables files for Amharic input.

%package arabic
Summary:        SCIM tables for Arabic
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description arabic
This package contains scim-tables files for Arabic input.

%if %{indic_tables}
%package bengali
Summary:        SCIM tables for Bengali
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description bengali
This package contains scim-tables files for Bengali input.
%endif

%package chinese
Summary:        SCIM tables for Chinese
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description chinese
This package contains scim-tables files for Chinese input.

%package chinese-extra
Summary:        Additional SCIM tables for Chinese
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description chinese-extra
This package contains additional less used scim-tables files for Chinese input.

%if %{indic_tables}
%package gujarati
Summary:        SCIM tables for Gujarati
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description gujarati
This package contains scim-tables files for Gujarati input.

%package hindi
Summary:        SCIM tables for Hindi
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description hindi
This package contains scim-tables files for Hindi input.
%endif

%if %{jk_tables}
%package japanese
Summary:        SCIM tables for Japanese
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description japanese
This package contains scim-tables files for Japanese.
%endif

%if %{indic_tables}
%package kannada
Summary:        SCIM tables for Kannada
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description kannada
This package contains scim-tables files for Kannada input.
%endif

%if %{jk_tables}
%package korean
Summary:        SCIM tables for Korean
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description korean
This package contains scim-tables files for Korean.
%endif

%if %{indic_tables}
%package malayalam
Summary:        SCIM tables for Malayalam scripts
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description malayalam
This package contains scim-tables files for Malayalam languages.
%endif

%if %{indic_tables}
%package marathi
Summary:        SCIM tables for Marathi
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description marathi
This package contains scim-tables files for Marathi input.
%endif


%package nepali
Summary:        SCIM tables for Nepali
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description nepali
This package contains scim-tables files for Nepali input.

%if %{indic_tables}
%package punjabi
Summary:        SCIM tables for Punjabi
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description punjabi
This package contains scim-tables files for Punjabi input.
%endif

%package russian
Summary:        SCIM tables for Russian
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description russian
This package contains scim-tables files for Russian input.

%if %{indic_tables}
%package tamil
Summary:        SCIM tables for Tamil
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description tamil
This package contains scim-tables files for Tamil input.
%endif

%package thai
Summary:        SCIM tables for Thai
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description thai
This package contains scim-tables files for Thai input.

%if %{indic_tables}
%package telugu
Summary:        SCIM tables for Telugu
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description telugu
This package contains scim-tables files for Telugu input.
%endif

%package ukrainian
Summary:        SCIM tables for Ukrainian
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description ukrainian
This package contains scim-tables files for Ukrainian input.

%package vietnamese
Summary:        SCIM tables for Vietnamese
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description vietnamese
This package contains scim-tables files for Vietnamese input.

%package additional
Summary:        Other miscellaneous SCIM tables
Group:          System Environment/Libraries
Requires:       scim-tables = %{version}

%description additional
This package contains some miscellaneous scim-tables.


%prep
%setup -q
%{__cp} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{_builddir}/%{name}-%{version}/tables/zh/


%patch1 -p1 -b .1-217639
%patch2 -p1 -b .2-232860

%build
autoreconf -ivf
intltoolize --force
autoreconf
%configure --disable-static
make  %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install

# kill *.a and *.la files
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/scim-1.0/*/*/*.la

# Insert CangJie5 icon mod.
%{__cp} %{SOURCE5} ${RPM_BUILD_ROOT}/%{_datadir}/scim/icons/

%if !%{indic_tables}
rm ${RPM_BUILD_ROOT}/%{_datadir}/scim/{icons,tables}/{Bengali,Gujarati,Hindi,Kannada,Malayalam,Marathi,Punjabi,Tamil,Telugu}-*
%endif

%if !%{jk_tables}
rm ${RPM_BUILD_ROOT}/%{_datadir}/scim/{icons,tables}/{Hangul,Hanja,HIRAGANA,KATAKANA,Nippon}*
%endif


%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-, root, root, -)
%{_bindir}/scim-make-table
%{_libdir}/scim-1.0/*/IMEngine/table.so
%{_libdir}/scim-1.0/*/SetupUI/table-imengine-setup.so
%{_datadir}/scim/icons/table.png
%dir %{_datadir}/scim/tables
%{_mandir}/man1/scim-make-table.1*


%files amharic
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Amharic.bin
%{_datadir}/scim/icons/Amharic.png


%files arabic
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Arabic.bin
%{_datadir}/scim/icons/Arabic.png


%if %{indic_tables}
%files bengali
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Bengali-inscript.bin
%{_datadir}/scim/tables/Bengali-probhat.bin
%{_datadir}/scim/icons/Bengali-inscript.png
%{_datadir}/scim/icons/Bengali-probhat.png
%endif

%files chinese
%defattr(-, root, root, -)
%doc tables/zh/README-*.txt
%{_datadir}/scim/tables/Array30.bin
%{_datadir}/scim/icons/Array30.png
%{_datadir}/scim/tables/CangJie3.bin
%{_datadir}/scim/icons/CangJie3.png
%{_datadir}/scim/tables/CangJie5.bin
%{_datadir}/scim/icons/CangJie5.png
%{_datadir}/scim/tables/CantonHK.bin
%{_datadir}/scim/icons/CantonHK.png
%{_datadir}/scim/tables/Quick.bin
%{_datadir}/scim/icons/Quick.png
%{_datadir}/scim/tables/Wubi.bin
%{_datadir}/scim/icons/Wubi.png
%{_datadir}/scim/tables/ZhuYin.bin
%{_datadir}/scim/icons/ZhuYin.png

%files chinese-extra
%defattr(-, root, root, -)
%doc tables/zh/README-*.txt
%{_datadir}/scim/tables/CNS11643.bin
%{_datadir}/scim/icons/CNS11643.png
%{_datadir}/scim/tables/CangJie.bin
%{_datadir}/scim/icons/CangJie.png
%{_datadir}/scim/tables/Cantonese.bin
%{_datadir}/scim/icons/Cantonese.png
%{_datadir}/scim/tables/Dayi3.bin
%{_datadir}/scim/icons/Dayi.png
%{_datadir}/scim/tables/EZ-Big.bin
%{_datadir}/scim/icons/EZ.png
%{_datadir}/scim/tables/Erbi.bin
%{_datadir}/scim/icons/Erbi.png
%{_datadir}/scim/tables/Erbi-QS.bin
%{_datadir}/scim/icons/Erbi-QS.png
%{_datadir}/scim/tables/Jyutping.bin
%{_datadir}/scim/icons/Jyutping.png
%{_datadir}/scim/tables/Simplex.bin
%{_datadir}/scim/icons/Simplex.png
%{_datadir}/scim/tables/SmartCangJie6.bin
%{_datadir}/scim/icons/SmartCangJie6.png
%{_datadir}/scim/tables/Stroke5.bin
%{_datadir}/scim/icons/Stroke5.png
%{_datadir}/scim/tables/Wu.bin
%{_datadir}/scim/icons/Wu.png
%{_datadir}/scim/tables/ZhuYin-Big.bin
%{_datadir}/scim/icons/ZhuYin.png
%{_datadir}/scim/tables/Ziranma.bin
%{_datadir}/scim/icons/Ziranma.png


%if %{indic_tables}
%files gujarati
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Gujarati-inscript.bin
%{_datadir}/scim/tables/Gujarati-phonetic.bin
%{_datadir}/scim/icons/Gujarati-inscript.png
%{_datadir}/scim/icons/Gujarati-phonetic.png

%files hindi
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Hindi-inscript.bin
%{_datadir}/scim/tables/Hindi-phonetic.bin
%{_datadir}/scim/icons/Hindi-inscript.png
%{_datadir}/scim/icons/Hindi-phonetic.png
%endif

%if %{jk_tables}
%files japanese
%defattr(-, root, root, -)
%doc tables/ja/kanjidic*
%{_datadir}/scim/tables/HIRAGANA.bin
%{_datadir}/scim/tables/KATAKANA.bin
%{_datadir}/scim/tables/Nippon.bin
%{_datadir}/scim/icons/HIRAGANA.png
%{_datadir}/scim/icons/KATAKANA.png
%{_datadir}/scim/icons/Nippon.png
%endif


%if %{indic_tables}
%files kannada
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Kannada-inscript.bin
%{_datadir}/scim/tables/Kannada-kgp.bin
%{_datadir}/scim/icons/Kannada-inscript.png
%{_datadir}/scim/icons/Kannada-kgp.png
%endif

%if %{jk_tables}
%files korean
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Hangul.bin
%{_datadir}/scim/tables/HangulRomaja.bin
%{_datadir}/scim/tables/Hanja.bin
%{_datadir}/scim/icons/Hangul.png
%{_datadir}/scim/icons/Hanja.png
%endif


%if %{indic_tables}
%files malayalam
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Malayalam-inscript.bin
%{_datadir}/scim/icons/Malayalam-inscript.png
%endif

%if %{indic_tables}
%files marathi
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Marathi-remington.bin
%{_datadir}/scim/icons/Marathi-remington.png
%endif

%files nepali
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Nepali_*.bin
%{_datadir}/scim/icons/Nepali.png


%if %{indic_tables}
%files punjabi
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Punjabi-inscript.bin
%{_datadir}/scim/tables/Punjabi-jhelum.bin
%{_datadir}/scim/tables/Punjabi-phonetic.bin
%{_datadir}/scim/icons/Punjabi-inscript.png
%{_datadir}/scim/icons/Punjabi-jhelum.png
%{_datadir}/scim/icons/Punjabi-phonetic.png
%endif


%files russian
%defattr(-, root, root, -)
%{_datadir}/scim/tables/RussianTraditional.bin
%{_datadir}/scim/tables/Yawerty.bin
%{_datadir}/scim/tables/Translit.bin
%{_datadir}/scim/icons/RussianTraditional.png
%{_datadir}/scim/icons/Yawerty.png
%{_datadir}/scim/icons/Translit.png


%if %{indic_tables}
%files tamil
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Tamil-inscript.bin
%{_datadir}/scim/tables/Tamil-phonetic.bin
%{_datadir}/scim/icons/Tamil-inscript.png
%{_datadir}/scim/icons/Tamil-phonetic.png
%endif


%files thai
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Thai.bin
%{_datadir}/scim/icons/Thai.png


%if %{indic_tables}
%files telugu
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Telugu-inscript.bin
%{_datadir}/scim/icons/Telugu-inscript.png
%endif


%files ukrainian
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Ukrainian-Translit.bin
%{_datadir}/scim/icons/Ukrainian-Translit.png


%files vietnamese
%defattr(-, root, root, -)
%{_datadir}/scim/tables/Viqr.bin
%{_datadir}/scim/icons/Viqr.png


%files additional
%defattr(-, root, root, -)
%{_datadir}/scim/tables/classicalhebrew.bin
%{_datadir}/scim/tables/greekpoly.bin
%{_datadir}/scim/tables/IPA-X-SAMPA.bin
%{_datadir}/scim/tables/IPA-Kirshenbaum.bin
%{_datadir}/scim/tables/LaTeX.bin
%{_datadir}/scim/tables/Uyghur-Romanized.bin
%{_datadir}/scim/tables/Uyghur-Standard.bin
%{_datadir}/scim/icons/IPA-X-SAMPA.png
%{_datadir}/scim/icons/LaTeX.png
%{_datadir}/scim/icons/Uyghur.png

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.5.12-5
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Ding-Yi Chen <dchen@redhat.com> - 0.5.12-1
- Upstream Update to 0.5.12
- Fixed 926498

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-6
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.5.9-4
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May  2 2009 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- update to 0.5.9
- scim-tables-0.5.8-1.gcc.patch upstream
- new RussianTraditional table

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Caius Chance <cchance@redhat.com> - 0.5.8-7
- Resolves: rhbz#461092 (Create specific CangJie 5 icon.)

* Thu Aug 28 2008 Caius Chance <cchance@redhat.com> - 0.5.8-6
- Resolves: rhbz#459772 (Update CangJie 5 table.)
- Turned on dynamic candidate order (frequency).

* Thu Aug 28 2008 Caius Chance <cchance@redhat.com> - 0.5.8-5
- Resolves: rhbz#460505 (Update Cantonese table.)

* Wed Aug 27 2008 Jens Petersen <petersen@redhat.com> - 0.5.8-4.fc10
- move the Chinese tables disabled by default in scim to a new chinese-extra
  subpackage
- move removal of Japanese tables from scim-tables-0.5.8-1.jk.patch to install

* Tue Jun 24 2008 Jens Petersen <petersen@redhat.com>
- remove Translit from ukrainian

* Mon Jun 23 2008 Jens Petersen <petersen@redhat.com> - 0.5.8-3.fc10
- update the license field to GPLv2+
- use canonical source url for sourceforge
- fix conditioning of patches

* Thu Jun 19 2008 Caius Chance <cchance@redhat.com> - 0.5.8-2.fc10
- Resolves: rhbz#438662 (Reverted Zhu Yin tables to previous version.)
- Rearrange Ukrainian IME as individual group.
- Reapply patch of bz#217639.
- Refined previous jk_tables patch.
- Arranged patch order.

* Mon Mar 31 2008 Caius Chance <cchance@redhat.com> - 0.5.8.1.fc9
- Update sources to 0.5.8.
- Applied certain patches in 0.5.7.
- Grouped Translit (Russian) and Ukrainian Translit IME to subpackages.

* Wed Feb 13 2008 Caius Chance <cchance@redhat.com> - 0.5.7-4.fc9
- Rebuild for F9.

* Tue Apr 17 2007 Jens Petersen <petersen@redhat.com> - 0.5.7-3
- make the main package own the tables directory (#226399)

* Tue Mar 27 2007 Caius Chance <cchance@redhat.com> - 0.5.7-2.1
- Fixed bz#226399: Merge Review, scim-tables.

* Mon Mar 19 2007 Caius Chance <cchance@redhat.com> - 0.5.7-2
- Fixed bz#217639: scim-tables Chang-Jie preedit was not cleared after focus 
                   out then focus in.

* Fri Oct 27 2006 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- update to 0.5.7 release

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.6-7
- rebuild
- Add missing br automake, gettext, libtool

* Thu Apr 27 2006 Jens Petersen <petersen@redhat.com> - 0.5.6-5
- obsolete old scim-tables-{japanese,korean} subpackages

* Fri Mar 31 2006 Jens Petersen <petersen@redhat.com> - 0.5.6-4
- rebuild without libstdc++so7

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 0.5.6-3
- move iiimf-le-unit obsoletes to scim-m17n (#183305)
- disable Indian script tables for now: they are now in m17n-db
  - added 'indic_tables' switch to allow them to be built

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.6-2.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Jens Petersen <petersen@redhat.com> - 0.5.6-2
- build conditionally with libstdc++so7 preview library (#166041)
  - add with_libstdc_preview switch and tweak libtool to link against it
- update filelist since moduledir is now api-versioned

* Fri Jan 13 2006 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- update to 0.5.6 release
  - update tables-skip-ja-ko.patch
  - updates filelist for chinese tables

* Mon Dec 26 2005 Jens Petersen <petersen@redhat.com> - 0.5.5-2
- remove the Japanese and Korean tables and their subpackages with
  tables-skip-ja-ko.patch and 'jk_tables' switch.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Dec  7 2005 Jens Petersen <jens@juhp.dyndns.org> - 0.5.5-1
- 0.5.5 release
- update filelist

* Mon Nov 14 2005 Jens Petersen <petersen@redhat.com> - 0.5.4-2
- add obsoletes iiimf-le-unit for upgrades (#173071)

* Wed Nov  2 2005 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- upstream 0.5.4 release
  - indic-icons-1.tar.gz, scim-tables-indic.patch, thai-table.patch, and
    scim-tables-cvs-20051018.patch are no longer needed

* Tue Oct 18 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-7
- update to cvs head to fix various table issues: add
  scim-tables-cvs-20051018.patch

* Thu Oct  6 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-6
- require scim

* Thu Sep 22 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-5
- drop Hindi itrans table for now since it is missing vowels signs

* Thu Sep 15 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-4
- add a Thai table derived from m17n-db with a Thai icon
- separate the Indic tables and the additional language tables into separate
  language subpackages

* Tue Sep  6 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-3
- add 14 new Indic tables for Bengali, Gujarati, Hindi, Kannada, Malayalam,
  Punjabi, Tamil and Telugu in updated scim-tables-indic.patch
  - inscript tables are derived from iiimf unitle tables
  - new icons for all Indic tables by Amanpreet Singh Brar
  - Indic tables are now in new scim-tables-indic subpackage
- make {chinese,japanese,korean} subpackages obsolete {zh,ja,ko}
- make subpackages own {_datadir}/scim/tables

* Wed Aug 17 2005 Jeremy Katz <katzj@redhat.com> - 0.5.3-2
- rebuild for new cairo

* Wed Aug 17 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- 0.5.3 release
  - replace scim-tables-0.5.1-add-hindi.patch with scim-tables-indic.patch
  - update files lists for new tables (ipa, latex, nepali, wu)
- rename {zh,ja,ko} subpackages to {chinese,japanese,korean}

* Tue Aug  2 2005 Jens Petersen <petersen@redhat.com> - 0.5.1-4
- initial build for Fedora Core
- add Hindi inscript and phonetic tables and icon to additional tables

* Wed Jul 27 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com> -0.5.1-3
- Rebuild for scim-1.4.0

* Sat Jun 25 2005 Colin Charles <colin@fedoraproject.org> 0.5.1-2
- Fix download URL

* Fri Jun 3 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com> 0.5.1-1
- Initial packaging for Fedora Extras.

* Wed Jan 5 2005 James Su <suzhe@tsinghua.org.cn>
- Added Generic Table IMEngine module into this package.

* Sun Jun 20 2004 James Su <suzhe@tsinghua.org.cn>
- Added Amharic table.

* Mon Apr 05 2004 James Su <suzhe@tsinghua.org.cn>
- Updated Nippon table.
- Added Yawerty table for Russian.

* Fri Nov 28 2003 James Su <suzhe@turbolinux.com.cn>
- upgraded CangJie.txt.in, added README-CangJie.txt

* Tue Sep 02 2003 James Su <suzhe@turbolinux.com.cn>
- updated table format according to SCIM 0.8.0
- added icon files.

* Wed Feb 26 2003 James Su <suzhe@turbolinux.com.cn>
- updated table format according to SCIM 0.3.1.

* Mon Nov 04 2002 James Su <suzhe@turbolinux.com.cn>
- Initial release.
