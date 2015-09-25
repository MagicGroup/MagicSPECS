%global	gem_name	rdtool

%if 0%{?fedora} >= 21
%global	gem_minitest	rubygem(minitest4)
%else
%global	gem_minitest	rubygem(minitest)
%endif

Name:		rubygem-%{gem_name}
Version:	0.6.38
Release:	7%{?dist}

Summary:	Formatter for RD
# From README.rd
# Note that setup.rb is not included in the binary
# rpm
License:	GPLv2+ or Ruby
URL:		https://github.com/uwabami/rdtool
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	%gem_minitest
BuildRequires:	rubygem(test-unit)
Requires:	ruby(release)
Requires:	ruby(rubygems)
BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
RD is multipurpose documentation format created for documentating Ruby and
output of Ruby world. You can embed RD into Ruby script. And RD have neat
syntax which help you to read document in Ruby script. On the other hand, RD
have a feature for class reference.


%package	doc
Summary:	Documentation for %{name}
# utils/rd-mode.el is under GPLv2+
License:	(GPLv2+ or Ruby) and GPLv2+
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# rename rdswap.rb
mv bin/rdswap{.rb,}
sed -i -e "s|rdswap\.rb|rdswap|" %{gem_name}.gemspec

# shebang
sed -i \
	-e '\@/usr/bin/env@d' \
	lib/rd/rd2html-ext-opt.rb
sed -i \
	-e 's|/usr/bin/ruby[^ ][^ ]*|%{_bindir}/ruby|' \
	bin/*

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
	Gemfile Rakefile \
	setup.rb \
	%{gem_name}.gemspec \
	test/

rm -f lib/rd/pre-setup.rb
find lib/rd -type f -print0 | xargs -0 chmod ugo-x
popd

%check
pushd .%{gem_instdir}
ruby -Ilib:test:. -e 'gem "minitest", "<5" ; Dir.glob("test/test-*.rb").each {|f| require f}'
popd

%files
%dir %{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/LGPL-2.1

%{_bindir}/rd2
%{_bindir}/rdswap

%{gem_instdir}/bin
%{gem_libdir}/

%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/doc/
%{gem_instdir}/utils/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.6.38-7
- 为 Magic 3.0 重建

* Tue Jun 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.38-6
- BR: rubygem(test-unit)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.38-4
- Force to use minitest ver4 for now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.38-2
- Incorporate comments on review request (bug 1031316)

* Thu Nov 14 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.6.38-1
- Initial package
