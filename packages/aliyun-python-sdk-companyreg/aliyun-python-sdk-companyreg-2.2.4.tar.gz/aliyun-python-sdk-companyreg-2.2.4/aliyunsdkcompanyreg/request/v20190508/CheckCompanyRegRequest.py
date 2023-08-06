# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkcompanyreg.endpoint import endpoint_data

class CheckCompanyRegRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'companyreg', '2019-05-08', 'CheckCompanyReg')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_OrgType(self): # String
		return self.get_query_params().get('OrgType')

	def set_OrgType(self, OrgType):  # String
		self.add_query_param('OrgType', OrgType)
	def get_IndustryType(self): # String
		return self.get_query_params().get('IndustryType')

	def set_IndustryType(self, IndustryType):  # String
		self.add_query_param('IndustryType', IndustryType)
	def get_TradeName(self): # String
		return self.get_query_params().get('TradeName')

	def set_TradeName(self, TradeName):  # String
		self.add_query_param('TradeName', TradeName)
	def get_City(self): # String
		return self.get_query_params().get('City')

	def set_City(self, City):  # String
		self.add_query_param('City', City)
	def get_NameType(self): # Integer
		return self.get_query_params().get('NameType')

	def set_NameType(self, NameType):  # Integer
		self.add_query_param('NameType', NameType)
