%global gem_name rdiscount

Summary: Fast Implementation of Gruber's Markdown in C
Name: rubygem-%{gem_name}
Version: 2.1.7.1
Release: 10%{?dist}
Group: Development/Languages
License: ASL 1.1
URL: http://github.com/rtomayko/rdiscount
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: libmarkdown-devel
BuildRequires: rubygem(test-unit)


%package doc
Summary: Documentation for %{name}
Group: Documentation
BuildArch: noarch
Requires: %{name} = %{version}-%{release}


%description
Description: Discount is an implementation of John Gruber's Markdown markup
language in C. It implements all of the language described in the markdown
syntax document and passes the Markdown 1.0 test suite.

#--

%description doc
This package contains Rakefile, test directory and documentation for
%{name}.


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby | sed -e 's|,|,\n|g' > %{gem_name}.gemspec

sed -i ext/extconf.rb \
	-e '\@check_sizeof@s| == 4|== size|'

# Remove files in discount-2.1.7
cat >> discount_files<<EOF
Csio.c
amalloc.c
basename.c
css.c
docheader.c
dumptree.c
emmatch.c
flags.c
generate.c
github_flavoured.c
html5.c
main.c
makepage.c
markdown.c
mkd2html.c
mkdio.c
mktags.c
pgm_options.c
resource.c
setup.c
tags.c
theme.c
toc.c
xml.c
xmlpage.c
mkdio.h
EOF

cat discount_files | while read f ; do
	rm -f ext/$f
	sed -i %{gem_name}.gemspec -e "\@ext/$f@d"
done

sed -i ext/extconf.rb \
	-e '\@create_makefile@i \$libs = "-lmarkdown"' \
	%{nil}

%build
rm -rf ./%{gem_extdir_mri}
rm -rf ./%{gem_instdir}
gem build %{gem_name}.gemspec

%gem_install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man7
mv .%{gem_instdir}/man/rdiscount.1 %{buildroot}%{_mandir}/man1
mv .%{gem_instdir}/man/markdown.7 %{buildroot}%{_mandir}/man7
cp -a .%{gem_dir}/*  %{buildroot}%{gem_dir}

# Copy C extensions to the extdir
rm -rf %{buildroot}%{gem_instdir}/ext
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

mkdir -p %{buildroot}/%{_bindir}
mv .%{_bindir}/* %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%check
pushd .%{gem_instdir}
# Once 
ruby -Ilib:ext:. \
	-e 'gem "test-unit" ; Dir.glob("test/*_test.rb").sort.each {|f| require f}' || :

remove_fail_test() {
	filename=$1
	shift
	num=$#
	while [ $num -gt 0 ]
	do
		if [ ! -f ${filename}.orig ] ; then
			cp -p $filename ${filename}.orig
		fi
		start=$(cat -n $filename | sed -n -e "\@^[ \t]*[1-9][0-9]*[ \t]*def $1@p" | sed -e 's|^[ \t]*||' -e 's|def.*$||')
		end=$(cat -n $filename | sed -n -e "\@^[ \t]*[1-9][0-9]*[ \t]*def $1@,\@^[ \t]*[1-9][0-9]*[ \t]*def@p" | tail -n 1 | sed -e 's|^[ \t]*||' -e 's|def.*$||')
		end=$((end - 1))
		sed -i -e "${start},${end}d" $filename
		shift
		num=$((num - 1))
	done
}
# test_that_extra_definition_lists_work needs --with-dl=Both is added to discount configure option
# test_that_tags_can_have_dashes_and_underscores needs --with-github-tags is added to discount configure option
remove_fail_test test/rdiscount_test.rb test_that_extra_definition_lists_work test_that_tags_can_have_dashes_and_underscores
ruby -Ilib:ext:. \
	-e 'gem "test-unit" ; Dir.glob("test/*_test.rb").sort.each {|f| require f}'

popd

%files
%{_bindir}/rdiscount
%dir %{gem_instdir}
%{gem_instdir}/bin/
%{gem_libdir}/
%doc %{gem_instdir}/BUILDING
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.markdown
%exclude %{gem_cache}
%{gem_spec}
%{gem_extdir_mri}/
%{_mandir}/man1/rdiscount.1.gz
%exclude %{_mandir}/man7/markdown.7.gz

#--

%files doc
%doc %{gem_instdir}/Rakefile
%{gem_docdir}
%{gem_instdir}/man
%{gem_instdir}/test
%{gem_instdir}/rdiscount.gemspec


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.7.1-10
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.7.1-9
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.7.1-7
- Recent usage of %%gem_install to modify source
- Use system libmarkdown

* Thu Jan 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.7.1-6
- Simply use test-unit

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7.1-2
- Rebuilt for Ruby_2.1

* Fri Apr 25 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7.1-1
- Update to 2.1.7.1

* Thu Apr 17 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Thu Feb 20 2014 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.1.7-1
- Update to 2.1.7

* Wed May 22 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7.3-1
- Update to 2.0.7.3
- Exclude man-page /usr/share/man/man7/markdown.7.gz

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.7-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 18 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-4
- Changed from ruby(abi) to ruby(release)
- Changed from macro gem_extdir to gem_extdir_mri

* Wed Feb 13 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-3
- Changed back to ruby(abi)

* Thu Feb 07 2013 Gerd Pokorra <gp@zimt.uni-siegen.de> - 2.0.7-1
- Update to 2.0.7
- Add file BUIlDING

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.6.3.2-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 12 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-4
- removed the unused macro "ruby_sitelib"
- put the file rdiscount.gemspec to the doc-subpackage
- add dependency to the main package for the doc-subpackage

* Thu Jun 10 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-3
- changed ruby(abi) dependency to be strict
- changed rubygem module related dependency style
- only arch-dependent files are in "ruby_sitearch"
- tests are now successful; "rake test:unit" is used
- "geminstdir" macro is used when possible
- "geminstdir" is owned by package
- ext/ subdirectory is removed form "buildroot" during install; no exclude

* Tue Jun 08 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-2
- files under ext/ subdirectory excluded
- remove BuildRoot tag
- add "Requires: ruby(abi) >= 1.8"
- use global macro instead of define macro
- changed license tag

* Sun Jun 06 2010 Gerd Pokorra <gp@zimt.uni-siegen.de> - 1.6.3.2-1
- add "BuildRequires: ruby-devel"
- Initial package
