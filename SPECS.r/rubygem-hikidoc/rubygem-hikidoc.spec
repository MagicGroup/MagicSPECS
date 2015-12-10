# Generated from hikidoc-0.0.6.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name	hikidoc

Name:		rubygem-%{gem_name}
Version:	0.1.0
Release:	6%{?dist}

Summary:	Text-to-HTML conversion tool for web writers
License:	MIT
URL:		https://github.com/hiki/hikidoc
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest)
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch:	noarch

Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
'HikiDoc' is a text-to-HTML conversion tool for web writers. 
HikiDoc allows you to write using an easy-to-read, easy-to-write plain 
text format, then convert it to structurally valid HTML (or XHTML).

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Encoding
for f in  \
	NEWS.ja \
	README.ja \
	TextFormattingRules.ja
do
	iconv -f EUC-JP -t UTF-8 -o $f{.utf,}
	touch -r $f{,.utf}
	mv $f{.utf,}
done

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
	.gitignore Gemfile Rakefile \
	%{gem_name}.gemspec \
	setup.rb \
	.travis.yml \
	test/
popd

%check
pushd .%{gem_instdir}

%if 0%{?fedora} >= 21
sed -i.minitest \
	-e 's|Test::Unit::TestCase|Minitest::Test|' \
	test/*.rb
cat > test/unit.rb << EOF
gem "minitest"
require "minitest/unit"
EOF
%endif

for f in test/*_test.rb
do
	ruby -Ilib:test:. $f
done
popd

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{_bindir}/hikidoc
%{gem_instdir}/bin

%{gem_libdir}/
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.1.0-6
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.1.0-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-1
- 0.1.0

* Thu Nov 14 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.0.6-1
- Initial package
