%global	gem_name	unf
%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	Wrapper library to bring Unicode Normalization Form support to Ruby/JRuby
Name:		rubygem-%{gem_name}
Version:	0.1.4
Release:	6%{?dist}

Group:		Development/Languages
License:	BSD
URL:		https://github.com/knu/ruby-unf
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby
%endif

Requires:	ruby(rubygems) 
Requires:	rubygem(unf_ext) 
BuildRequires:	rubygems-devel 
# %%check
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(shoulda)
BuildRequires:	rubygem(unf_ext)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
This is a wrapper library to bring Unicode Normalization Form support
to Ruby/JRuby.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

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

%check
pushd .%{gem_instdir}
sed -i.orig \
	-e '/begin/,/end/d' \
	-e '/bundler/d' \
	test/helper.rb

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e 's|Test::Unit::TestCase|Minitest::Test|' \
	test/*.rb
cat > test/unit.rb << EOF
gem "minitest"
require "minitest/autorun"
EOF

%endif

for f in test/test_*.rb
do
	ruby -Ilib:test:. $f
done
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{gem_libdir}/
%exclude	%{gem_cache}
%{gem_spec}

%exclude	%{gem_instdir}/*.gemspec
%exclude	%{gem_instdir}/.gitignore
%exclude	%{gem_instdir}/.travis.yml

%files	doc
%doc	%{gem_docdir}
%exclude	%{gem_instdir}/test/

%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.4-5
- F-21 shoulda is now 3.5.0, fix test case

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.4-3
- Use minitest/autorun instead of minitest/unit

* Thu Apr 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.4-2
- Support Minitest 5.x

* Wed Apr  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.4-1
- 0.1.4

* Sun Oct 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.3-1
- 0.1.3

* Thu Oct  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.2-1
- 0.1.2

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.1-1
- 0.1.1

* Fri Mar 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-1
- 0.1.0

* Sat Jan 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.5-1
- Initial package
