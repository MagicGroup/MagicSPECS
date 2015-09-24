%global	gem_name	levenshtein
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Calculates the Levenshtein distance between two byte strings
Name:		rubygem-%{gem_name}
Version:	0.2.2
Release:	8%{?dist}

Group:		Development/Languages
# LICENSE file
License:	GPLv2
URL:		http://www.erikveen.dds.nl/levenshtein/doc/index.html
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)
Requires:	ruby(rubygems) 
BuildRequires:	rubygems-devel 
BuildRequires:	ruby-devel
BuildRequires:	rubygem(minitest)
Provides:	rubygem(%{gem_name}) = %{version}

%description
Calculates the Levenshtein distance between two byte strings.

The Levenshtein distance is a metric for measuring the amount
of difference between two sequences (i.e., the so called edit
distance). The Levenshtein distance between two sequences is
given by the minimum number of operations needed to transform
one sequence into the other, where an operation is an
insertion, deletion, or substitution of a single element.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# Permission
find . -name \*.rb -print0 | xargs --null chmod 0644

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%if 0%{?fedora} >= 21
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

pushd %{buildroot}
rm -f .%{gem_extdir_mri}/{gem_make.out,mkmf.log}
popd

%else
mkdir -p %{buildroot}%{gem_extdir_mri}/lib
mv \
	%{buildroot}%{gem_instdir}/lib/levenshtein \
	%{buildroot}%{gem_extdir_mri}/lib/

%endif

# Remove the binary extension sources and build leftovers.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e 's|Test::Unit::TestCase|Minitest::Test|' \
	test/*.rb
cat > test/unit.rb << EOF
gem "minitest"
require "minitest/autorun"
EOF
%endif

ruby \
%if 0%{?fedora} >= 21
	-Ilib:.:ext/%{gem_name} \
%else
	-Ilib \
%endif
	test/test.rb
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{gem_libdir}/
%{gem_extdir_mri}/
%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%exclude	%{gem_instdir}/test/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-7
- F-22: Rebuild for ruby 2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-4
- F-21: rebuild for ruby 2.1 / rubygems 2.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-2
- F-19: Rebuild for ruby 2.0.0

* Sat Jan  5 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.2.2-1
- Initial package
