%global gem_name expression_parser

Name: rubygem-%{gem_name}
Version: 0.9.0
Release: 7%{?dist}
Summary: A math parser
Group: Development/Languages
License: MIT
URL: http://lukaszwrobel.pl/blog/math-parser-part-3-implementation
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# License is in upstream Git master, but not yet shipped in a released gem.
# https://raw.github.com/nricciar/expression_parser/master/MIT-LICENSE
Source1: rubygem-expression_parser-MIT-LICENSE
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A math parser


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

rm Rakefile
sed -i "s|\"Rakefile\",||g" %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

install -m 0644 -p %{SOURCE1} %{buildroot}%{gem_instdir}/MIT-LICENSE

%check
pushd .%{gem_instdir}
  rspec parser_spec.rb
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/parser_spec.rb

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.9.0-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.9.0-6
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 21 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-4
- Correct MIT-LICENSE file permissions

* Tue Nov 19 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-3
- Remove macro in comment
- Remove email transcripts
- Add MIT-LICENSE file from upstream

* Mon Nov 18 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-2
- Include email transcripts describing MIT license.

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.9.0-1
- Initial package
